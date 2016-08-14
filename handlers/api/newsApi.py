# -*-coding:utf-8-*-
__author__ = 'howie,jeezy'
import tornado.web
import hashlib
import json
import  datetime,time
import random
from config.n_conf import admin
from methods.pDb import newsDb
from system.classPredict.main import startPredict
from system.latentFactor.geneCalcul import GeneCulcal

import os
from system.pointsAlo.scoreSetting import ScoreTool


class Confirm(tornado.web.RequestHandler):
    # time=1 tooken=764bfd755bc07f6871eee104219b2b2c
    def tooken(self, time):
        tooken = "apiNews"
        tooken = hashlib.md5((tooken + str(time)).encode("utf-8")).hexdigest()
        return tooken

    def write_error(self, status_code, **kwargs):
        self.write("错误状态码{0}.\n".format(
            status_code))

    def errorRequest(self, num):
        data = {"flag": num}
        result = {"message": "failed", "data": data}
        result = json.dumps(result)
        self.write(result)

    def set_default_headers(self):
        self.set_header ('Access-Control-Allow-Origin', '*')
        self.set_header ('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header ('Access-Control-Max-Age', 1000)
        self.set_header ('Access-Control-Allow-Headers', '*')

class Register(Confirm):
    # 注册
    def get(self, *args, **kwargs):
        all = self.request.arguments
        name = self.get_argument('name')
        passwd = self.get_argument('passwd')
        phone = self.get_argument('phone')
        tags = self.get_argument('tags')
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        if getTooken == tooken and len(all) == 6:
            passwd = hashlib.md5((admin["TOKEN"] + passwd).encode("utf-8")).hexdigest()

            db = newsDb()
            is_register = db.select_table(table = "user", column = "*", condition = "phone", value = phone)
            if is_register:
                # 用户已存在
                self.errorRequest(num=-1)
            else:
                try:
                    num = db.select_table_two(table = "user", column = "count(*)")
                    user_id = ("%06d" % (num[0][0] + 1))

                    insertSql = db.insert_table(table="user", field="(user_id,phone,name,passwd,time)",
                                                  values="('" + str(
                                                      user_id) + "','" + phone + "','" + name + "','" + passwd + "',now())")
                    user_messSql = db.insert_table(table="user_mess", field="(user_id)",
                                                     values="('" + str(user_id) + "')")
                    loveTageSql = db.insert_table (table="user_love_tag", field="(user_id,tags)",
                                                      values="('" + str (user_id) + "','" + tags + "')")
                    user_mess = db.select_table(table = "user", column = "user_id", condition = "phone", value = phone)

                    #**********    分数    ***************************************************************************************

                    db.insert_table(table = "user_tag_score",field="",values="('" + user_id + "',1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)")
                    print("start")

                    #gc = GeneCulcal()
                    #gc.getMatData()
                    print("end")
                    print(user_mess[0][0])
                    if insertSql and user_messSql and loveTageSql:
                        data = {"user_id": user_mess[0][0]}
                        result = {"message": "success", "data": data}
                        result = json.dumps(result)
                        self.write(result)
                except:
                    # 出现错误则回滚
                    print("404")
        else:
            self.errorRequest(num=0)


class Login(Confirm):
    # 登录
    def get(self, *args, **kwargs):
        all = self.request.arguments
        passwd = self.get_argument('passwd')
        phone = self.get_argument('phone')
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        if getTooken == tooken and len(all) == 4:
            db = newsDb ()
            passwd = hashlib.md5((admin["TOKEN"] + passwd).encode("utf-8")).hexdigest()
            information = db.select_table(table = "user", column = "*", condition = "phone", value = phone)
            try:
                user_mess = db.select_table(table="user", column="user_id", condition="phone", value=phone)
                if information:
                    if information[0][3] == passwd:
                        # 登录成功
                        data = {"user_id": user_mess[0][0]}
                        result = {"message": "success", "data": data}
                        result = json.dumps(result)
                        self.write(result)
                    else:
                        # 密码错误
                        self.errorRequest(num=-1)
                else:
                    # 用户不存在
                    self.errorRequest(num=-2)
            except:
                # 出现错误则回滚
                print("404")
        else:
            self.errorRequest(num=0)


class NewsTags(Confirm):
    # 新闻列表请求
    def get(self, *args, **kwargs):
        all = self.request.arguments
        count = self.get_argument('count')
        alrequest = self.get_argument('alrequest')
        user_id = self.get_argument('userid')
        tag = self.get_argument('tag')
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        data = []
        if (getTooken == tooken and len(all) == 6) or (getTooken == tooken and len(all) == 7) :

            db = newsDb()
            # 通过用户id在推荐表中寻找要推荐的新闻id
            information = db.select_table(table = "news_recommend", column = "*", condition = "user_id", value =user_id )
            try:
                if user_id !="" and user_id !=" ":
                    if information:
                    # 得到该用户的推荐新闻
                        if information[0][1].count("$"):
                            allNews = information [0] [1].split ('$')
                            amalen = information[0][1].count("$")
                            news = allNews[amalen].split ('#')

                        else:
                            news = information [0] [1].split ('#')
                        lenght = len (news)
                        news_id = ''

                        if int (alrequest) + int (count) > len (news):
                            # 请求大于有效值
                            self.errorRequest (num=-1)
                        else:
                            if tag == '':
                                suiji = {random.randint (int(alrequest), int(alrequest) + int(count)) for _ in range (int (count))}
                                for i in range(int(alrequest), int(alrequest) + int(count)):
                                    news_id = news[i].split('+')[0]
                                    data.append(self.dataNews(news_id))
                            else:
                                id_list = db.select_table_three("select news_id from get_news where tag = '"+tag+"' order by news_id")
                                if len(id_list) < int(alrequest) + int(count):
                                    suiji = {random.randint (int(alrequest), len(id_list)) for _ in
                                             range ((len(id_list)-int(alrequest)))}
                                    for j in range(int(alrequest), len(id_list)):
                                        # print(self.dataNews (id_list[j][0]))
                                        data.append(self.dataNews(id_list[j][0]))
                                else:
                                    suiji = {random.randint (int(alrequest), int(alrequest) + int(count)) for _ in
                                             range (int(count))}
                                    for j in range(int(alrequest), int(alrequest) + int(count)):
                                        # print(self.dataNews (id_list[j][0]))
                                        data.append(self.dataNews(id_list[j][0]))


                    else:
                        #刚注册用户
                        love_tags = db.select_table_three("select tags from user_love_tag where user_id = '"+user_id+"'")
                        re_news = []
                        eng_tags = ('news_society','news_entertainment','news_tech','news_car','news_sports','news_finance','news_military','news_world','news_fashion','news_travel','news_discovery','news_baby','news_regimen','news_story','news_essay','news_game','news_history','news_food')
                        chi_tags = ('社会','娱乐','科技','汽车','体育','财经','军事','国际','时尚','旅游','探索','育儿','养生','故事','美文','游戏','历史','美食')
                        select_tag = ''
                        if tag=='':
                            for retag in love_tags[0]:
                                if retag.count(","):
                                    tag_list=retag.split(',')
                                    for ta in tag_list:
                                        for i in range(0,len(eng_tags)):
                                            if chi_tags[i] == ta:
                                                select_tag = eng_tags[i]
                                        each_news = db.select_table_three("select news_id from get_news where tag = '"+select_tag+"'")
                                        if len(each_news) >=20:
                                            for d in range(0,20):
                                                re_news.append(each_news[d][0])
                                        else:
                                            for d in range(0,len(each_news)):
                                                re_news.append(each_news[d][0])
                                else:
                                    for i in range(0, len(eng_tags)):
                                        if chi_tags[i] == love_tags[0][0]:
                                            select_tag = eng_tags[i]
                                    each_news = db.select_table_three("select news_id from get_news where tag = '" + select_tag + "'")

                                    if len(each_news) >= 20:
                                        for d in range(0, 20):
                                            re_news.append(each_news[d][0])
                                    else:
                                        for d in range(0, len(each_news)):
                                            re_news.append(each_news[d][0])
                            if len(re_news) >=int (count):
                                suiji = {random.randint(0,len(re_news)-1) for _ in range(int (count))}
                            else:
                                suiji = {random.randint (0, len (re_news) - 1) for _ in range (len (re_news) - 1)}

                            for n in suiji:
                                data.append(self.dataNews(re_news[n]))
                        else:
                            id_list = db.select_table (table="get_news", column="news_id", condition="tag",
                                                       value=tag)
                            if len (id_list) < int (alrequest) + int (count):
                                for j in range (int (alrequest), len (id_list)):
                                    # print(self.dataNews (id_list[j][0]))
                                    data.append (self.dataNews (id_list [j] [0]))
                            else:
                                for j in range (int (alrequest), int (alrequest) + int (count)):
                                    # print(self.dataNews (id_list[j][0]))
                                    data.append (self.dataNews (id_list [j] [0]))




                else:
                    if tag:
                        id_list = db.select_table(table="get_news",column="news_id",condition="tag",value=tag)
                    else:
                        id_list = db.select_table_two(table="get_news",column="news_id")
                    if len(id_list) < int (alrequest) + int (count):
                        for j in range (int (alrequest),len(id_list)):
                            # print(self.dataNews (id_list[j][0]))
                            data.append (self.dataNews (id_list [j] [0]))
                    else:
                        for j in range(int (alrequest),int (alrequest)+int(count)):
                            #print(self.dataNews (id_list[j][0]))
                            data.append (self.dataNews (id_list[j][0]))
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                #print(data[0])
                self.write(result)
            except:
                # 出现错误则回滚
                print("404")
        else:
            self.errorRequest(num=0)

    def dataNews(self,news_id):
        db = newsDb ()
        read_times = 0
        love_times = 0
        comment_times = 0
        image = ""
        news_content = db.select_table (table="get_news", column="news_id,title,time,source,image,abstract",
                                              condition="news_id ",value=news_id)
        opData = db.select_table (table="news_mess", column="read_times,love_times,comment_times",
                                          condition="news_id ",value=news_id)

        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        startTime = (str(localtime).split(' '))[0]
        each = startTime.split('-')
        timeTwo = int(each[2])
        if timeTwo > 10:
            times = each[0] + "-" + each[1] + "-" + str(timeTwo)
        else:
            times = each[0] + "-" + each[1] + "-" + "0" + str(timeTwo)

        oldTimeList = str(news_content[0][2]).split(' ')
        oldTimeDate = oldTimeList[0].split('-')
        d1 = datetime.datetime(int(oldTimeDate[0]), int(oldTimeDate[1]), int(oldTimeDate[2]))
        d2 = datetime.datetime(int(each[0]), int(each[1]), int(each[2]))


        cdate = (d2 - d1).days
        if cdate == 0:
            oldHours = oldTimeList[1].split(':')[0]
            eachHours = (str(localtime).split(' '))[1].split(':')[0]
            chineseTime = str(int(eachHours)-int(oldHours)) + "小时前"
        elif cdate == 1:
            chineseTime = "昨天"
        elif cdate == 2:
            chineseTime = "前天"
        else:
            chineseTime = str((d2 - d1).days) + "天前"
            #chineseTime = str(int(((d2 - d1).seconds) / 3600)) + "小时前"


        if opData:
            read_times = opData[0][0]
            love_times = opData[0][1]
            comment_times = opData[0][2]
        if news_content [0][4].count("http://") > 1:
            for i in range(0,len(news_content [0][4].split(","))):
                if (news_content [0][4].split(","))[i].count("icon")<1:
                    image = (news_content [0][4].split(","))[i]
                    break
            #print(image)
        else:
            if news_content [0][4].count("icon")<1:
                image = news_content [0][4]

        data={"news_id": news_content [0][0], "title": news_content [0][1], "time": chineseTime, "source": news_content [0] [3],
             "image": image, "abstract": news_content [0] [5], "read_times": read_times,
             "love_times": love_times, "comment_times": comment_times}
        #print(data)
        return data


class NewsContent(Confirm):
    # 返回新闻内容
    def get(self, *args, **kwargs):
        all = self.request.arguments
        news_id = self.get_argument('newsid')
        user_id = self.get_argument('userid')
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        message = []
        relate_list = []
        is_love = 0
        time = ''
        uname = ''
        head_url = ''
        is_comment = ''
        comment_content = ''
        if getTooken == tooken and len(all) == 4:
            db = newsDb()
            news = db.select_table(table="get_news",column="html_content,news_link",condition="news_id",value=news_id)
            messageall = db.select_table(table="news_comment",column="*",condition="news_id",value=news_id)
            relate = db.select_table_three("select tag from get_news where news_id = '"+news_id+"'")
            tag =  relate[0][0]
            all_relate = db.select_table_three("select news_id,title from get_news where tag ='"+tag+"'")
            ar = random.sample(all_relate,3)
            for i in range(0,len(ar)):
                relate_list.append({"news_id":ar[i][0],"news_title":ar[i][1]})
            print(relate_list)
            try:
                news_content = news[0][0]
                news_url = news[0][1]

                #print(messageall[0][1])
                if user_id:
                    userBehavior = db.select_table (table="user_behavior", column="is_comment,behavior_type",
                                                    condition="user_id",
                                                    value=user_id + "' and news_id = '" + news_id)
                    if userBehavior:

                        if userBehavior[0][0]:
                            is_comment = userBehavior [0] [0]
                        else:
                            is_comment = 0
                        if userBehavior[0][1] == 1:
                            is_love = 1
                        else:
                            is_love = 0
                # {##}每条新闻详情
                if messageall:
                    if messageall[0][1]:
                        allComment= messageall[0][1].split("{##}")
                        for i in range(0,len(allComment)-1):
                            me = allComment[i].split("{++}")
                            times = str(me[2])
                            comment_content = me[1]
                            # 通过用户编号查询用户评论的昵称和头像
                            com_username = db.select_table(table="user,user_mess",column="user.name,user_mess.image",condition="user.user_id",
                                                           value=me[0] + "' and user_mess.user_id = '" + me[0])
                            if com_username[0][1]:
                                head_url = com_username[0][1]
                            else:
                                head_url = ""
                            uname = com_username[0][0]
                            message.append({"head_url": head_url,"user_id":me[0], "username": uname, "comment_time": times,"comment_content":comment_content,"dianzan_num":me[3]})

                data = {"news_id":news_id,"content":news_content ,"news_url":news_url, "is_comment": is_comment, "is_love": is_love, "comment_list": message,"relate_list":relate_list}

                print("data success!")
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                self.write(result)
                #****阅读相关数据库更新
                if user_id:
                    timescore = db.select_table(table = "user_behavior", column = "times,score", condition = "news_id", value = news_id + "' and user_id = '" + user_id)
                    #print("haha")
                    #print(timescore)
                    tag = db.select_table (table="get_news", column="tag", condition="news_id", value=news_id)

                    if timescore:
                        #mSql.update_column(table = "user_behavior",column = "times",value_set = times, condition = "user_id",value_find = user_id + "' and news_id = '" +news_id)
                        db.exeSql("update user_behavior set times= times + 1 where user_id= '"+user_id+"' and news_id ='" +news_id+ "'")
                    else:
                        db.insert_table(table = "user_behavior", field = "(user_id,news_id,news_tag,times)", values = "('" +user_id+ "','" +news_id+ "','" +tag[0][0]+ "',1)")




                #设置老新闻
                db.exeSql ("update get_news set is_old= 1 where news_id= '" + news_id + "'")
                # 设置新闻基本信息表阅读次数
                read_times = db.select_table(table = "news_mess", column = "read_times", condition = "news_id", value = news_id)
                if read_times:
                    db.exeSql ("update news_mess set read_times= read_times + 1 where news_id= '" + news_id + "'")

                else:
                    tag = db.select_table(table="get_news", column="tag", condition="news_id", value=news_id)
                    db.insert_table (table="news_mess", field="(news_id,tag,read_times)",
                                       values="('"  +news_id + "','" + tag [0] [0] + "',1)")


                #************************用户标签因子历史分数****************************
                all_tags = ('news_society','news_entertainment','news_tech','news_car','news_sports','news_finance','news_military','news_world','news_fashion','news_travel','news_discovery','news_baby','news_regimen','news_story','news_essay','news_game','news_history','news_food')

                tag = db.select_table(table="get_news", column="tag", condition="news_id", value=news_id)

                if_news_deep = db.select_table(table="news_tag_deep", column="*", condition="news_id", value=news_id)

                upda_sql = " "
                if if_news_deep:
                    for i in range(0,len(all_tags)):

                        if upda_sql==" ":
                            upda_sql = upda_sql + all_tags[i] + " = " + all_tags[i] + " + " + str(if_news_deep[0][i+1])
                        else:
                            upda_sql = upda_sql + "," + all_tags [i] + " = " + all_tags [i] + " + " + str(if_news_deep [0] [i+1])

                    if_tag_deep = db.select_table_three("select * from user_tag_score where user_id='"+ user_id+"'")
                    if if_tag_deep:
                        jiafen = db.exeSql("update user_tag_score set "+upda_sql+" where user_id ='"+user_id+"'")
                    else:
                        in_sql = "'" + user_id + "'"
                        num = len (all_tags)+1
                        for i in range (0, len (all_tags)):
                            in_sql = in_sql + "," + str(if_news_deep[0][i+1])

                        jiafen = db.exeSql("insert into user_tag_score values("+in_sql+")")
                    if jiafen:
                        print("阅读加分成功!")




            except:
                # 出现错误则回滚
                print("404")
        else:
            self.errorRequest(num=0)


class UserInfo(Confirm):
    # 查询返回用户信息
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument('userid')
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        if getTooken == tooken and len(all) == 3:
            db = newsDb()
            userSql = "select name,phone from user where user_id = '" + user_id + "'"
            userInfoSql = "select * from user_mess where user_id = '" + user_id + "'"
            love_timesSql = "select * from user_operate where user_id = '" + user_id + "'"
            readSql = "select times,is_comment from user_behavior where user_id = '" + user_id + "'"
            try:

                # 提交到数据库执行,得到用户电话
                user = db.select_table_three(userSql)

                # 提交到数据库执行,得到用户详情
                userInfo = db.select_table_three(userInfoSql)
                # 查询用户行为
                love = db.select_table_three(love_timesSql)

                # 查询阅读
                allRead = db.select_table_three(readSql)
                read_times = 0
                message_times = 0
                if allRead:
                    for each in allRead:
                        if each[0]:
                            read_times = read_times + each [0]
                        if each [1] == 1:
                            message_times = message_times + 1

                if userInfo [0] [3]:
                    email = userInfo [0] [3]
                else:
                    email=""
                data = {"user_name": user [0] [0], "phone": user [0] [1], "email": email,
                        "image": userInfo [0] [5],
                        "read_times": read_times, "love_times": len (love), "message_times": message_times}
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
            except:
                # 出现错误则回滚
                print("404")

        else:
            self.errorRequest (num=0)

class UserInfoChange(Confirm):
    # 用户更改个人信息
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument ('userid')
        user_name = self.get_argument('username')
        image = self.get_argument('image')
        email = self.get_argument('email')
        getTooken = self.get_argument ('tooken')
        time = self.get_argument ('time')
        tooken = self.tooken (time=time)
        if getTooken == tooken and len (all) == 6:
            db = newsDb()
            try:
               db.update_column(table = "user",column = "name",value_set = user_name, condition  = "user_id",value_find = user_id)
               db.update_column (table="user_mess", column="email", value_set=email, condition="user_id",value_find=user_id)
               db.update_column (table="user_mess", column="image", value_set=image, condition="user_id",value_find=user_id)
               data=self.select(user_id)
               result = {"message": "success", "data": data}
               result = json.dumps (result)
               self.write (result)
            except:
                # 出现错误则回滚
                print("404")
        else:
            self.errorRequest (num=0)

    def select(self,user_id):
        db = newsDb()
        # 提交到数据库执行,得到用户电话
        user = db.select_table(table="user",column="name,phone",condition="user_id",value=user_id)
        # 提交到数据库执行,得到用户详情
        userInfo = db.select_table(table="user_mess",column="*",condition="user_id",value=user_id)
        # 查询用户行为

        love =  db.select_table(table="user_operate",column="*",condition="user_id",value=user_id)
        # 查询阅读

        allRead =  db.select_table(table="user_behavior",column="times,is_comment",condition="user_id",value=user_id)
        read_times = 0
        message_times = 0
        for each in allRead:
            read_times = each [0]
            if each [1] == 1:
                message_times = message_times + 1
        data = {"user_name": user [0] [0], "phone": user [0] [1], "email": userInfo [0] [3],
                "image": userInfo [0] [5],
                "read_times": read_times, "love_times": len (love), "message_times": message_times}
        return data

class LoveNews(Confirm):
    # 喜欢功能
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument ('userid')
        is_love = self.get_argument('islove')
        news_id = self.get_argument('newsid')
        getTooken = self.get_argument ('tooken')
        retime = self.get_argument ('time')
        tooken = self.tooken (time=retime)
        if (getTooken == tooken and len (all) == 5) or (getTooken == tooken and len (all) == 6):
            db = newsDb()
            localtime = time.strftime ("%Y-%m-%d %H:%M:%S", time.localtime ())
            try:
                behavior_type = db.select_table(table = "user_behavior", column = "behavior_type", condition = "news_id", value = news_id + "' and user_id = '" +user_id)

                if behavior_type[0][0] == 1 and is_love == '1':
                    self.errorRequest (num=-1)
                else:
                    #用户喜欢
                    success = False
                    if is_love == '1':
                        tag = db.select_table(table = "get_news", column = "tag", condition = "news_id", value = news_id)
                        love_times = db.select_table(table = "news_mess", column = "love_times", condition = "news_id", value = news_id)
                        love_times = love_times[0][0] +1
                        tag_point = db.select_table(table = "user_tag_score", column = tag[0][0], condition = "user_id", value = user_id)

                        #*****************用户行为表的更新******************************
                        timescore = db.select_table (table="user_behavior", column="times,score", condition="news_id",
                                                       value=news_id + "' and user_id = '" + user_id)

                        if timescore:
                            # ******************************新闻分数******************************
                            update_love = db.update_column (table="user_behavior", column="behavior_type",
                                                              value_set='1', condition="news_id ",
                                                              value_find=news_id + "' and user_id = '" + user_id)

                        else:
                            # ******************************新闻分数******************************
                            db.insert_table (table="user_behavior", field="(user_id,news_id,news_tag,score,times)",
                                               values="('" + user_id + "','" + news_id + "','" + tag [0] [0] + "',3,1)")



                        #查询user _behavior表是否有该用户和新闻
                        is_operate = db.select_table(table = "user_operate", column = "*", condition = "news_id ", value = news_id + "' and user_id = '" +user_id)
                        #更新用户操作表
                        if is_operate:
                            operate_islove = db.update_column (table ="user_operate" , column = "is_love",value_set = '1',condition = "news_id ", value_find = news_id + "' and user_id = '" +user_id )
                            operate_time = db.update_column (table="user_operate", column="time", value_set=localtime,condition="news_id ",value_find=news_id + "' and user_id = '" + user_id)
                        else:
                            insert_operate = db.insert_table(table = "user_operate", field = "(user_id,news_id,is_love,time)", values = "('" +user_id+ "','" +news_id+ "','1','" +localtime+ "')")

                        #更新新闻基本信息表
                        update_mess = db.update_column (table ="news_mess" , column = "love_times",value_set = str(love_times),condition = "news_id ", value_find = news_id )

                        #********************更新用户标签因子分数（历史分数）******************************

                        all_tags = (
                        'news_society', 'news_entertainment', 'news_tech', 'news_car', 'news_sports', 'news_finance',
                        'news_military', 'news_world', 'news_fashion', 'news_travel', 'news_discovery', 'news_baby',
                        'news_regimen', 'news_story', 'news_essay', 'news_game', 'news_history', 'news_food')

                        tag = db.select_table (table="get_news", column="tag", condition="news_id", value=news_id)

                        if_news_deep = db.select_table (table="news_tag_deep", column="*", condition="news_id",
                                                        value=news_id)

                        upda_sql = " "
                        if if_news_deep:
                            for i in range (0, len (all_tags)):

                                if upda_sql == " ":
                                    upda_sql = upda_sql + all_tags [i] + " = " + all_tags [i] + " + " + str (
                                        if_news_deep [0] [i + 1]*3)
                                else:
                                    upda_sql = upda_sql + "," + all_tags [i] + " = " + all_tags [i] + " + " + str (
                                        if_news_deep [0] [i + 1]*3)

                            if_tag_deep = db.select_table_three (
                                "select * from user_tag_score where user_id='" + user_id + "'")
                            if if_tag_deep:
                                jiafen = db.exeSql (
                                    "update user_tag_score set " + upda_sql + " where user_id ='" + user_id + "'")
                            else:
                                in_sql = "'" + user_id + "'"
                                num = len (all_tags) + 1
                                for i in range (0, len (all_tags)):
                                    in_sql = in_sql + "," + str (if_news_deep [0] [i + 1]*3)
                                jiafen = db.exeSql ("insert into user_tag_score values(" + in_sql + ")")
                            if jiafen:
                                print ("喜欢加分成功!")

                        success = 1

                    #****************************用户取消喜欢*************************************************************
                    elif is_love == '0':

                        all_tags = (
                            'news_society', 'news_entertainment', 'news_tech', 'news_car', 'news_sports',
                            'news_finance',
                            'news_military', 'news_world', 'news_fashion', 'news_travel', 'news_discovery', 'news_baby',
                            'news_regimen', 'news_story', 'news_essay', 'news_game', 'news_history', 'news_food')

                        tag = db.select_table (table="get_news", column="tag", condition="news_id", value=news_id)

                        if_news_deep = db.select_table (table="news_tag_deep", column="*", condition="news_id",
                                                        value=news_id)

                        upda_sql = " "
                        if if_news_deep:
                            for i in range (0, len (all_tags)):

                                if upda_sql == " ":
                                    upda_sql = upda_sql + all_tags [i] + " = " + all_tags [i] + " - " + str (
                                        if_news_deep [0] [i + 1] * 3)
                                else:
                                    upda_sql = upda_sql + "," + all_tags [i] + " = " + all_tags [i] + " - " + str (
                                        if_news_deep [0] [i + 1] * 3)

                            if_tag_deep = db.select_table_three (
                                "select * from user_tag_score where user_id='" + user_id + "'")
                            jiafen = db.exeSql (
                                    "update user_tag_score set " + upda_sql + " where user_id ='" + user_id + "'")

                            if jiafen:
                                print ("取消喜欢减分成功!")







                        db.update_column(table="user_behavior", column="behavior_type",
                                           value_set='0', condition="news_id ",
                                           value_find=news_id + "' and user_id = '" + user_id)
                        tag = db.select_table (table="get_news", column="tag", condition="news_id", value=news_id)
                        love_times = db.select_table (table="news_mess", column="love_times", condition="news_id", value=news_id)
                        print(love_times)
                        love_time = love_times [0] [0] + 1
                        print(love_time)
                        tag_point = db.select_table (table="user_tag_score", column=tag [0] [0], condition="user_id",
                                                       value=user_id)

                        # 更新用户操作表
                        operate_islove = db.update_column (table="user_operate", column="is_love", value_set='0',
                                                     condition="news_id ",value_find=news_id + "' and user_id = '" + user_id)
                        operate_time = db.update_column (table="user_operate", column="time", value_set="",
                                                   condition="news_id ", value_find=news_id + "' and user_id = '" + user_id)
                        print("ga")

                        # 更新新闻基本信息表
                        upNews_mess = "update news_mess set love_times = love_times - 1 where news_id = '" + news_id + "'"
                        db.exeSql(upNews_mess)

                        # ********************更新用户标签因子分数（历史分数）******************************
                        #user_tag_points =  mSql.update_column (table ="user_tag_score" , column = tag[0][0],value_set = tag[0][0] +" - 1",condition = "user_id ", value_find = user_id )
                        success = 2
                    else:
                        self.errorRequest (num=0)
                        success = 0
                    if success:
                        data = {"flag": success}
                        result = {"message": "success", "data": data}
                        result = json.dumps (result)
                        self.write (result)
            except:
                # 出现错误则回滚
                print("404")

        else:
            self.errorRequest (num=0)

class LoveList(Confirm):
    # 查询返回用户历史喜欢新闻列表
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument ('userid')
        getTooken = self.get_argument ('tooken')
        retime = self.get_argument ('time')
        tooken = self.tooken (time=retime)
        if getTooken == tooken and len (all) == 3:
            #print("ha")

            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            startTime = (str(localtime).split(' '))[0]
            each = startTime.split('-')
            timeTwo = int(each[2])
            if timeTwo > 10:
                times = each [0] + "-" + each [1] + "-" + str (timeTwo)
            else:
                times = each[0] + "-" + each[1] + "-" + "0" + str(timeTwo)
            try:
                db = newsDb()
                love_listSql = "select news_id,time from user_operate where is_love = 1 " \
                               "and TIMESTAMPDIFF(DAY,time,'" +times+ "') < 60 and user_id = '" +user_id+ "' order by time desc"

                # 提交到数据库执行
                love_list = db.select_table_three(love_listSql)
                data = []
                for item in love_list:
                    getNews = db.select_table(table = "get_news", column = "title,abstract,time", condition = "news_id", value = item[0])
                    each_get_news = getNews[0]

                    oldTimeList = str (each_get_news [2]).split(' ')
                    oldTimeDate = oldTimeList[0].split('-')
                    d1 = datetime.datetime (int(oldTimeDate[0]), int(oldTimeDate[1]), int(oldTimeDate[2]))
                    d2 = datetime.datetime (int(each[0]), int(each[1]), int(each[2]))

                    cdate = (d2-d1).days
                    if cdate == 0:
                        chineseTime = "今天"
                    elif cdate == 1 :
                        chineseTime = "今天"
                    elif cdate == 2 :
                        chineseTime = "昨天"
                    elif cdate == 2:
                        chineseTime = "前天"
                    else:
                        chineseTime = oldTimeDate[1] + "."+ oldTimeDate[2]

                    news_mess = db.select_table(table = "news_mess", column = "*", condition = "news_id", value = item[0])
                    image = db.select_table(table = "get_news", column = "image", condition = "news_id", value = item[0])
                    tag = db.select_table(table = "news_tag_chinese", column = news_mess[0][1], condition = "'1'", value = "1")
                    #print(image)
                    if image[0][0]:
                        if image[0][0].count("http://") >1:
                            images = (image[0][0].split(","))[0]
                            #print(image)
                        else:
                            images = image[0][0]
                    else:
                        images = ''

                    #print("haha")
                    if news_mess:
                        data.append({"news_id":news_mess[0][0],"tag":tag[0][0],"image":images,"read_times":news_mess[0][2],"love_times":news_mess[0][3],
                                     "comment_times":news_mess[0][4],"title":each_get_news[0],"abstract":each_get_news[1],"time":chineseTime})
                print(data)
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
            except:
                # 出现错误则回滚
                print("404")

        else:
            self.errorRequest (num=0)


class HotList(Confirm):
    # 查询返回热点新闻
    def get(self, *args, **kwargs):
        all = self.request.arguments
        hot_type = self.get_argument ('hot')
        count = self.get_argument('count')
        alrequest = self.get_argument('alrequest')
        getTooken = self.get_argument ('tooken')
        time = self.get_argument ('time')
        tooken = self.tooken (time=time)
        if getTooken == tooken and len (all) == 5:
            db = newsDb()
            sqlcount = db.select_table(table = "news_hot", column = "news_id", condition = "'1'", value = "1")
            if int (alrequest) == len (sqlcount):
                self.errorRequest (num=-1)
            else:
                if int (alrequest) + int (count) > len(sqlcount):
                    self.loveList (hot_type, str(len(sqlcount)-int(alrequest)), alrequest)

                else:
                    self.loveList(hot_type,count,alrequest)

        else:
            self.errorRequest (num=0)

    def loveList(self,hot_type,count,alrequest):
        try:
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            startTime = (str(localtime).split(' '))[0]
            each = startTime.split('-')
            timeTwo = int(each[2])
            if timeTwo > 10:
                start = each [0] + "-" + each [1] + "-" + str (timeTwo)
            else:
                start = each[0] + "-" + each[1] + "-" + "0" +str(timeTwo)
            if hot_type == "1":
                self.love(start,count,alrequest)
            elif hot_type =="2":
                self.read(start,count,alrequest)
            elif hot_type == "3":
                self.comment(start,count,alrequest)
            else:
                self.errorRequest (num=0)
        except:
            # 出现错误则回滚
            print("404")


    def love(self,times,count,alrequest):
        db = newsDb()
        data = []
        #print("love")
        try:
            #allLove = mSql.select_table(table = "hot", column = "news_id,tag,love_times,read_times,comment_times", condition = "1", value = "1 order by love_times desc")
            listSql = "select news_id,tag,image,love_times,read_times,comment_times,abstract," \
                      "source,title,time from news_hot where TIMESTAMPDIFF(DAY,time,'" +times+ "') < 2 order by love_times desc"
            #print(listSql)

            # 提交到数据库执行
            allLove = db.select_table_three(listSql)



            for j in range (int (alrequest), int (alrequest) + int (count)):
                # print(self.dataNews (id_list[j][0]))
                love = allLove[j]
                tag = db.select_table (table="news_tag_chinese", column=love [1], condition="'1'", value="1")
                print(love[2])
                if love[2]:
                    if love[2].count ("http://") > 1:
                        image = (love[2].split (",")) [0]
                        # print(image)
                    else:
                        image = love[2]
                else:
                    image = ''

                chinese = self.chinese_time(love[0])
                print(chinese)
                data.append({"news_id":love[0],"tag":tag[0][0],"image":image,"love_times":love[3],"read_times":love[4],"comment_times":love[5],"abstract":love[6],"source":love[7],"title":love[8],"time":chinese})
                print(data)
            result = {"message": "success", "data": data}
            result = json.dumps (result)
            self.write (result)
        except:
            self.errorRequest (num=0)
    def read(self,time,count,alrequest):
        db = newsDb()
        data = []
        #print("read")
        try:
            # allLove = mSql.select_table(table = "hot", column = "news_id,tag,love_times,read_times,comment_times", condition = "1", value = "1 order by love_times desc")
            listSql = "select news_id,tag,image,love_times,read_times,comment_times,abstract," \
                      "source,title from news_hot where TIMESTAMPDIFF(DAY,time,'" + time + "') < 2 order by read_times desc"
            # print(listSql)
            # 提交到数据库执行
            allLove = db.select_table_three(listSql)
            for j in range (int (alrequest), int (alrequest) + int (count)):
                # print(self.dataNews (id_list[j][0]))
                love = allLove [j]
                tag = db.select_table(table = "news_tag_chinese", column = love [1], condition = "'1'", value = "1")
                if love [2]:
                    if love [2].count ("http://") > 1:
                        image = (love [2].split (",")) [0]
                        # print(image)
                    else:
                        image = love [2]
                else:
                    image = ''

                chinese = self.chinese_time(love[0])
                data.append ({"news_id": love [0], "tag": tag [0][0],"image":image,"love_times":love[3],"read_times":love[4],
                              "comment_times":love[5],"abstract":love[6],"source":love[7],"title":love[8],"time":chinese})

            result = {"message": "success", "data": data}
            result = json.dumps (result)
            self.write (result)
        except:
            self.errorRequest (num=0)
    def comment(self,time,count,alrequest):
        db = newsDb()
        data = []
        #print("commnet")
        try:
            # allLove = mSql.select_table(table = "hot", column = "news_id,tag,love_times,read_times,comment_times", condition = "1", value = "1 order by love_times desc")
            listSql = "select news_id,tag,image,love_times,read_times,comment_times,abstract," \
                      "source,title from news_hot where TIMESTAMPDIFF(DAY,time,'" + time + "') < 2 order by comment_times desc"
            # print(listSql)
            # 提交到数据库执行
            allLove = db.select_table_three(listSql)
            for j in range (int (alrequest), int (alrequest) + int (count)):
                # print(self.dataNews (id_list[j][0]))
                love = allLove [j]
                tag = db.select_table (table="news_tag_chinese", column=love [1], condition="'1'", value="1")
                if love [2]:
                    if love [2].count ("http://") > 1:
                        image = (love [2].split (",")) [0]
                        # print(image)
                    else:
                        image = love [2]
                else:
                    image = ''

                chinese = self.chinese_time(love[0])
                data.append ({"news_id": love [0], "tag": tag[0][0],"image":image,"love_times":love[3],"read_times":love[4],"comment_times":love[5],"abstract":love[6],"source":love[7],"title":love[8],"time":chinese})

            result = {"message": "success", "data": data}
            result = json.dumps (result)
            self.write (result)
        except:
            self.errorRequest (num=0)


    def chinese_time(self,news_id):
        db = newsDb()
        sql = "select time from news_hot where news_id = '" +news_id+ "'"
        da = db.select_table_three(sql)
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        startTime = (str(localtime).split(' '))[0]
        each = startTime.split('-')
        oldTimeList = str(da[0][0]).split(' ')
        oldTimeDate = oldTimeList[0].split('-')
        d1 = datetime.datetime(int(oldTimeDate[0]), int(oldTimeDate[1]), int(oldTimeDate[2]))
        d2 = datetime.datetime(int(each[0]), int(each[1]), int(each[2]))

        cdate = (d2 - d1).days
        if cdate == 0:
            oldHours = oldTimeList[1].split(':')[0]
            eachHours = (str(localtime).split(' '))[1].split(':')[0]
            chineseTime = str(int(eachHours) - int(oldHours)) + "小时前"
        elif cdate == 1:
            chineseTime = "今天"
        elif cdate == 2:
            chineseTime = "昨天"
        elif cdate == 2:
            chineseTime = "前天"
        else:
            chineseTime = str((d2 - d1).days) + "天前"

        return chineseTime




class FeedBack(Confirm):
    # 反馈
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument ('userid')
        feedBack = self.get_argument ('feedback')
        getTooken = self.get_argument ('tooken')
        retime = self.get_argument ('time')
        tooken = self.tooken (time=retime)
        if getTooken == tooken and len (all) == 4:
            db = newsDb()
            times = time.time()
            print(str(times))
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            try:

                db.insert_table(table = "news_feedback ", field = "(user_id,feedback,getTime)", values = "('" + user_id + "','" +feedBack+ "','"+ localtime +"')")
                data = {"flag": 1}
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
            except:
                # 出现错误则回滚
                print("404")
        else:
            self.errorRequest (num=0)

class KeyWord(Confirm):
    # 关键词搜索
    def get(self, *args, **kwargs):
        all = self.request.arguments
        keyWord = self.get_argument ('keyword')
        getTooken = self.get_argument ('tooken')
        retime = self.get_argument ('time')
        tooken = self.tooken (time=retime)
        data = []
        read_times = 0
        love_times = 0
        comment_times = 0
        if getTooken == tooken and len (all) == 3:
            db = newsDb()
            try:
                keySql = "select news_id from get_news where title like '%" +keyWord+ "%'"
                # 提交到数据库执行
                news_id_list = db.select_table_three(keySql)
                if len(news_id_list)>=20:
                    counts = 20
                else:
                    counts = len(news_id_list)
                for m in range(0,counts):
                    news_content = db.select_table (table="get_news",
                                                      column="news_id,title,time,source,image,abstract",
                                                      condition="news_id ", value=news_id_list[m][0])
                    opData = db.select_table (table="news_mess", column="read_times,love_times,comment_times",
                                                condition="news_id ", value=news_id_list[m][0])
                    if opData:
                        read_times = opData [0] [0]
                        love_times = opData [0] [1]
                        comment_times = opData [0] [2]
                    if news_content [0] [4].count ("http://") > 1:
                        image = (news_content [0] [4].split (",")) [0]
                        # print(image)
                    else:
                        image = news_content [0] [4]

                    localtime = time.strftime ("%Y-%m-%d %H:%M:%S", time.localtime ())
                    startTime = (str (localtime).split (' ')) [0]
                    each = startTime.split ('-')
                    oldTimeList = str (news_content[0][2]).split (' ')
                    oldTimeDate = oldTimeList [0].split ('-')
                    d1 = datetime.datetime (int (oldTimeDate [0]), int (oldTimeDate [1]), int (oldTimeDate [2]))
                    d2 = datetime.datetime (int (each [0]), int (each [1]), int (each [2]))

                    cdate = (d2 - d1).days
                    if cdate == 0:
                        oldHours = oldTimeList [1].split (':') [0]
                        eachHours = (str (localtime).split (' ')) [1].split (':') [0]
                        chineseTime = str (int (eachHours) - int (oldHours)) + "小时前"
                    elif cdate == 1:
                        chineseTime = "今天"
                    elif cdate == 2:
                        chineseTime = "昨天"
                    elif cdate == 2:
                        chineseTime = "前天"
                    else:
                        chineseTime = str ((d2 - d1).days) + "天前"



                    data.append({"news_id": news_content [0][0], "title": news_content [0][1], "time": chineseTime,
                                 "source": news_content [0] [3],"image": image, "abstract": news_content [0] [5], "read_times": read_times,
                                 "love_times": love_times, "comment_times": comment_times})
                #print(data)
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                # print(data[0])
                self.write (result)
            except:
                # 出现错误则回滚
                print("404")
        else:
            self.errorRequest (num=0)

class Comment(Confirm):
    # 评论
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument ('userid')
        news_id = self.get_argument ('newsid')
        content = self.get_argument("content")
        getTooken = self.get_argument ('tooken')
        retime = self.get_argument ('time')
        tooken = self.tooken (time=retime)
        localtime = time.strftime ("%Y-%m-%d %H:%M:%S", time.localtime ())
        comment = user_id + "{++}" + content + "{++}" + localtime + "{++}" + '0' + "{##}"
        news_comment = news_id + "{++}" + content + "{++}" + localtime  + "{##}"
        if (getTooken == tooken and len (all) == 5) or (getTooken == tooken and len (all) == 6):
            db = newsDb()
            try:
                tags = db.select_table(table = "get_news", column = "tag", condition = "news_id", value = news_id)
                tag = tags[0][0]
                is_comment = db.select_table(table = "news_comment", column = "comment", condition = "news_id", value = news_id)
                #print(is_comment)
                #如果该新闻已有评论
                if is_comment:
                    commentNew = is_comment[0][0] + comment
                    db.update_column(table = "news_comment",column = "comment",value_set = commentNew, condition = "news_id",value_find = news_id)
                #如果还没有评论
                else:
                    comment = user_id + "{++}" + content + "{++}" + localtime + "{++}" +'0' + "{##}"
                    db.insert_table(table = "news_comment", field = "(news_id,comment)", values = "('" + news_id + "','" + comment + "')")

                #****************************设置用户对应分数*******************************************
                upBehaviorSql = "update user_behavior set is_comment = 1,score = score + 2 " \
                                "where user_id = '" +user_id+ "' and news_id = '" +news_id+ "'"
                db.exeSql(upBehaviorSql)
                print ("评论成功，用户对此条新闻 分数 加1")

                #设置新闻基本信息表
                upNews_mess = "update news_mess set comment_times = comment_times + 1 where news_id = '"  + news_id + "'"
                db.exeSql(upNews_mess)
                print ("评论成功，用户对此条新闻 评论次数 加1")

                #设置用户操作表
                is_comment = db.select_table(table = "user_operate", column = "comment", condition = "user_id", value = user_id +"' and news_id = '" +news_id)
                if is_comment:
                    if is_comment[0][0]:
                        db.update_column (table="user_operate", column="comment",
                                            value_set= is_comment[0][0] + news_comment, condition="user_id",
                                            value_find=user_id + "' and news_id = '" + news_id)
                    else:
                        print("ha")
                        db.update_column(table = "user_operate",column = "comment",value_set = news_comment,
                                           condition = "user_id",value_find = user_id + "' and news_id = '" + news_id)
                else:
                    db.insert_table(table = "user_operate", field = "(user_id,news_id,comment,is_love,time)",
                                      values = "('" +user_id+ "','" +news_id+ "','" +news_comment+ "',0,'" +localtime +"')")
                print("评论成功，用户操作表更新")

                #*******************用户标签因子分数表对应该标签历史分数***************************
                all_tags = (
                'news_society', 'news_entertainment', 'news_tech', 'news_car', 'news_sports', 'news_finance',
                'news_military', 'news_world', 'news_fashion', 'news_travel', 'news_discovery', 'news_baby',
                'news_regimen', 'news_story', 'news_essay', 'news_game', 'news_history', 'news_food')

                tag = db.select_table (table="get_news", column="tag", condition="news_id", value=news_id)

                if_news_deep = db.select_table (table="news_tag_deep", column="*", condition="news_id", value=news_id)

                upda_sql = " "
                if if_news_deep:
                    for i in range (0, len (all_tags)):

                        if upda_sql == " ":
                            upda_sql = upda_sql + all_tags [i] + " = " + all_tags [i] + " + " + str (
                                if_news_deep [0] [i + 1]*2)
                        else:
                            upda_sql = upda_sql + "," + all_tags [i] + " = " + all_tags [i] + " + " + str (
                                if_news_deep [0] [i + 1]*2)

                    if_tag_deep = db.select_table_three ("select * from user_tag_score where user_id='" + user_id + "'")
                    if if_tag_deep:
                        jiafen = db.exeSql (
                            "update user_tag_score set " + upda_sql + " where user_id ='" + user_id + "'")
                    else:
                        in_sql = "'" + user_id + "'"
                        num = len (all_tags) + 1
                        for i in range (0, len (all_tags)):
                            in_sql = in_sql + "," + str (if_news_deep [0] [i + 1]*2)

                        jiafen = db.exeSql ("insert into user_tag_score values(" + in_sql + ")")
                    if jiafen:
                        print ("评论加分成功!")


                #查询评论的用户的个人信息返回
                image = db.select_table(table = "user_mess", column = "image", condition = "user_id", value = user_id)
                name = db.select_table (table="user", column="name", condition="user_id", value=user_id)
                data = {"user_id": user_id,"user_name":name[0][0],"user_image":image[0][0],"news_id":news_id,
                        "content":content,"comment_time":localtime}
                #print(data)
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
                print("success")
            except:
                # 出现错误则回滚
                print('404')
        else:
            self.errorRequest (num=0)

class LoveComment(Confirm):
    # 赞评论
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument ('userid')
        news_id = self.get_argument ('newsid')
        comment = self.get_argument("comment")
        comment_time = self.get_argument("commenttime")
        getTooken = self.get_argument ('tooken')
        retime = self.get_argument ('time')
        tooken = self.tooken (time=retime)
        #print(tooken)
        news_comment = ''
        new_love = ''
        if getTooken == tooken and len (all) == 6:
            db = newsDb()
            try:
                commentAllList = db.select_table(table = "news_comment", column = "*", condition = "news_id", value = news_id)
                commentAll = commentAllList[0][1].split("{##}")
                #print(commentAllList[0][1])
                for i in range(0,len(commentAll)-1):
                    each = commentAll[i].split("{++}")
                    if comment_time == each [2] and comment == each [1] and user_id == each[0]:
                        #print (each [3])
                        new_love = str(int (each [3])+ 1)
                        break
                for n in range (0, len (commentAll) - 1):
                    each = commentAll [n].split ("{++}")
                    if comment_time == each [2] and comment == each [1] and user_id == each[0]:
                        news_comment = news_comment + each[0] + "{++}" + each[1] + "{++}" + each[2] + "{++}" + new_love + "{##}"
                        #continue
                    else:
                        news_comment = news_comment + commentAll[n] + "{##}"
                        #continue
                db.update_column(table = "news_comment",column = "comment",value_set = news_comment, condition = "news_id",value_find = news_id)
                data = {"flag": 1}
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
            except:
                # 出现错误则回滚
                print("404")
        else:
            self.errorRequest (num=0)

class ExitRead(Confirm):
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument ('userid')
        news_id = self.get_argument ('newsid')
        time_diff = self.get_argument('timediff')
        getTooken = self.get_argument ('tooken')
        time = self.get_argument ('time')
        tooken = self.tooken (time=time)
        if getTooken == tooken and len (all) == 5:
            db = newsDb()
            try:
                db.update_column(table = "user_behavior",column = "weight",value_set = time_diff, condition = "user_id",value_find = user_id +"' and news_id = '"+ news_id)
                data = {"flag": 1}
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
            except:
                # 出现错误则回滚
                print ("404")

        else:
            self.errorRequest (num=0)

class ReturnTags(Confirm):
    def get(self, *args, **kwargs):
        all = self.request.arguments
        getTooken = self.get_argument ('tooken')
        time = self.get_argument ('time')
        tooken = self.tooken (time=time)
        if getTooken == tooken and len (all) == 2:
            try:
                data = [{"key":"news_society","name":"社会"},{"key":"news_entertainment","name":"娱乐"},{"key":"news_tech","name":"科技"},{"key":"news_car","name":"汽车"},{"key":"news_sports","name":"体育"},
                        {"key":"news_finance","name":"财经"},{"key":"news_military","name":"军事"},{"key":"news_world","name":"国际"}, {"key":"news_fashion","name":"时尚"},{"key":"news_travel","name":"旅游"},
                        {"key":"news_discovery","name":"探索"},{"key":"news_baby","name":"育儿"},{"key":"news_regimen","name":"养生"},{"key":"news_story","name":"故事"},
                        {"key":"news_essay","name":"美文"},{"key":"news_game","name":"游戏"},{"key":"news_history","name":"历史"},{"key":"news_food","name":"美食"}]
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
            except:
                # 出现错误则回滚
                print ("404")

        else:
            self.errorRequest (num=0)


class AdminUser(Confirm):
    def get(self, *args, **kwargs):
        all = self.request.arguments
        count = self.get_argument('count')
        alrequest = self.get_argument ('alrequest')
        page = self.get_argument('page')
        getTooken = self.get_argument ('tooken')
        time = self.get_argument ('time')
        tooken = self.tooken (time=time)
        data = []
        if (getTooken == tooken and len (all) == 5) or (getTooken == tooken and len (all) == 6):
            try:
                db = newsDb()
                user = db.select_table_three ("select user_id,name from user order by user_id")

                if page == "next":
                    if int(alrequest) >= len(user):
                        self.errorRequest (num=-1)
                    else:
                        if int(alrequest) + int(count) > len(user):
                            for i in range (int (alrequest), len(user)):
                                each_user = user [i]
                                info = {"user_id": each_user [0], "user_name": each_user [1]}
                                data.append (info)
                            result = {"message": "success", "data": data}
                            result = json.dumps (result)
                            self.write (result)
                        else:
                            for i in range(int(alrequest),int(count) + int(alrequest)):
                                each_user = user[i]
                                info = {"user_id":each_user[0],"user_name":each_user[1]}
                                data.append(info)
                            result = {"message": "success", "data": data}
                            result = json.dumps (result)
                            self.write (result)

                else:
                    for i in range (int (alrequest)-int(count),int (alrequest)):
                        each_user = user [i]
                        info = {"user_id": each_user [0], "user_name": each_user [1]}
                        data.append (info)
                    result = {"message": "success", "data": data}
                    result = json.dumps (result)
                    self.write (result)


            except:
                # 出现错误则回滚
                print ("404")

        else:
            self.errorRequest (num=0)


class AdminUserInfo(Confirm):
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument ('user_id')
        getTooken = self.get_argument ('tooken')
        time = self.get_argument ('time')
        tooken = self.tooken (time=time)
        if (getTooken == tooken and len (all) == 3) or (getTooken == tooken and len (all) == 4):
             db = newsDb ()
             info_1 = db.select_table_three("select phone from user where user_id='" +user_id+"'")
             info_2 = db.select_table_three("select sex,age,email,address from user_mess where user_id='" +user_id+"'")
             data={"phone":info_1[0][0],"sex":info_2[0][0],"age":info_2[0][1],"email":info_2[0][0],"address":info_2[0][0]}
             result = {"message": "success", "data": data}
             result = json.dumps (result)
             self.write (result)
        else:
            self.errorRequest (num=0)


class AdminFeedback(Confirm):
    def get(self, *args, **kwargs):
        all = self.request.arguments
        count = self.get_argument ('count')
        alrequest = self.get_argument ('alrequest')
        page = self.get_argument ('page')
        getTooken = self.get_argument ('tooken')
        time = self.get_argument ('time')
        tooken = self.tooken (time=time)
        data=[]
        if (getTooken == tooken and len (all) == 5) or (getTooken == tooken and len (all) == 6):
            db = newsDb()
            feedback = db.select_table_three("select user_id,feedback,getTime from news_feedback where isReply = 0")
            user_name = db.select_table_three("select name from user where user_id = '"+ feedback[0][0] +"'")

            if page == "xia":
                if int (alrequest) >= len (feedback):
                    self.errorRequest (num=-1)
                else:
                    if int (alrequest) + int (count) > len (feedback):
                        for i in range (int (alrequest), len (feedback)):
                            each_user = feedback [i]
                            user_name = db.select_table_three ("select name from user where user_id = '" + each_user[0] + "'")
                            info = {"user_id":each_user[0],"user_name":user_name[0][0],"contents":each_user[1],"times":"2016-07-11 15:11:21"}

                            data.append (info)
                        print (data)
                        result = {"message": "success", "data": data}
                        result = json.dumps (result)
                        self.write (result)
                    else:
                        for i in range (int (alrequest), int (count) + int (alrequest)):
                            each_user = feedback [i]
                            user_name = db.select_table_three (
                                "select name from user where user_id = '" + each_user [0] + "'")
                            info = {"user_id":each_user[0],"user_name":user_name[0][0],"contents":each_user[1],"times":"2016-07-11 15:11:21"}
                            data.append (info)
                        print (data)
                        result = {"message": "success", "data": data}
                        result = json.dumps (result)
                        self.write (result)

            else:
                for i in range (int (alrequest) - int (count), int (alrequest)):
                    each_user = feedback [i]
                    user_name = db.select_table_three ("select name from user where user_id = '" + each_user [0] + "'")
                    info = {"user_id":each_user[0],"user_name":user_name[0][0],"contents":each_user[1],"times":"2016-07-11 15:11:21"}
                    data.append (info)
                print (data)
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)

        else:
            self.errorRequest (num=0)