# -*-coding:utf-8-*-
__author__ = 'howie,jeezy'
import tornado.web
import hashlib
import json
import time
from config.n_conf import admin
import methods.db as mSql


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
            judge = "select * from user where phone = '" + phone + "'"
            mSql.cur.execute(judge)
            # 提交到数据库执行
            is_register = mSql.cur.fetchall()
            if is_register:
                # 用户已存在
                self.errorRequest(num=-1)
            else:
                numSql = " select count(*) from user"
                try:
                    mSql.cur.execute(numSql)
                    # 提交到数据库执行
                    num = mSql.cur.fetchall()
                    user_id = ("%06d" % (num[0][0] + 1))
                    insertSql = mSql.insert_table(table="user", field="(user_id,phone,name,passwd,time)",
                                                  values="('" + str(
                                                      user_id) + "','" + phone + "','" + name + "','" + passwd + "',now())")
                    user_messSql = mSql.insert_table(table="user_mess", field="(user_id)",
                                                     values="('" + str(user_id) + "')")
                    loveTageSql = mSql.insert_table (table="user_love_tag", field="(user_id,tags)",
                                                      values="('" + str (user_id) + "','" + tags + "')")
                    user_mess = mSql.select_table(table = "user", column = "user_id", condition = "phone", value = phone)
                    #print(user_mess[0][0])
                    if insertSql and user_messSql and loveTageSql:
                        data = {"user_id": user_mess[0][0]}
                        result = {"message": "success", "data": data}
                        result = json.dumps(result)
                        self.write(result)
                except:
                    # 出现错误则回滚
                    mSql.conn.rollback()
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
            passwd = hashlib.md5((admin["TOKEN"] + passwd).encode("utf-8")).hexdigest()
            numsqllogin = "select * from user where phone = '" + phone + "'"
            try:
                mSql.cur.execute(numsqllogin)
                # 提交到数据库执行
                information = mSql.cur.fetchall()
                user_mess = mSql.select_table(table="user", column="user_id", condition="phone", value=phone)
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
                mSql.conn.rollback()
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
        if getTooken == tooken and len(all) == 6:
            # 通过用户id在推荐表中寻找要推荐的新闻id
            recommend = "select * from news_recommend where user_id = '" + user_id + "'"
            try:
                if user_id:
                    mSql.cur.execute (recommend)
                    # 提交到数据库执行
                    information = mSql.cur.fetchall ()
                    # 得到该用户的推荐新闻
                    news = information [0] [1].split ('#')
                    lenght = len (news)
                    news_id = ''
                    print (lenght)
                    if int (alrequest) + int (count) > len (news):
                        # 请求大于有效值
                        self.errorRequest (num=-1)
                    else:
                        if tag == '':
                            for i in range (int (alrequest), int (alrequest) + int (count)):
                                news_id = news [i].split ('+') [0]
                                data.append (self.returnData (news_id))
                        else:
                            n = 0
                            for i in range (int (alrequest), lenght):
                                if n < int (count):
                                    news_id = news [i].split ('+') [0]
                                    if tag == news [i].split ('+') [1]:
                                        n = n + 1
                                        data.append (self.returnData (news_id))
                                    else:
                                        continue
                else:
                    if tag:
                        id_listSql = "select news_id from get_news where tag = '" + tag + "'"
                        mSql.cur.execute (id_listSql)
                        # 提交到数据库执行
                        id_list = mSql.cur.fetchall ()
                    else:
                        id_listSql = "select news_id from get_news"
                        mSql.cur.execute (id_listSql)
                        # 提交到数据库执行
                        id_list = mSql.cur.fetchall ()
                    #new = []
                    for j in range(int (alrequest),int (alrequest)+int(count)):
                        #print(self.dataNews (id_list[j][0]))
                        data.append (self.dataNews (id_list[j][0]))
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                #print(data[0])
                self.write(result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback()
        else:
            self.errorRequest(num=0)

    def returnData(self,news_id):
        data = []
        newsl = "select get_news.news_id,get_news.title,get_news.time,get_news.source," \
                "get_news.image,get_news.abstract,news_mess.read_times,news_mess.love_times," \
                "news_mess.comment_times from get_news,news_mess where get_news.news_id" \
                " = '" + news_id + "' and news_mess.news_id ='" + news_id + "'"
        mSql.cur.execute (newsl)
        # 提交到数据库执行
        new_list = mSql.cur.fetchall ()
        for each in new_list:
            # print(str(each[2]))
            # dateC = str(each[2])
            # timestamp = time.mktime (dateC)
            # print(timestamp)
            print(each[2])
            data.append (
                {'news_id': each [0], 'title': each [1], 'time': str(each[2]), 'source': each [3],
                 'image': each [4], 'abstract': each [5], 'read_times': each [6],
                 'love_times': each [7], 'comment_times': each [8]})
            #print(data)
            return data
    def dataNews(self,news_id):
        read_times = 0
        love_times = 0
        comment_times = 0
        news_content = mSql.select_table (table="get_news", column="news_id,title,time,source,image,abstract",
                                              condition="news_id ",value=news_id)
        opData = mSql.select_table (table="news_mess", column="read_times,love_times,comment_times",
                                          condition="news_id ",value=news_id)
        if opData:
            read_times = opData[0][0]
            love_times = opData[0][1]
            comment_times = opData[0][2]
        if news_content [0][4].count("http://") > 1:
            image = (news_content [0][4].split(","))[0]
            #print(image)
        else:
            image = news_content [0][4]
        #print(str(news_content[0][2]))
        #print(str(news_content))
        data={"news_id": news_content [0][0], "title": news_content [0][1], "time": str(news_content[0][2]), "source": news_content [0] [3],
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
        is_love = 0
        time = ''
        uname = ''
        head_url = ''
        is_comment = ''
        comment_content = ''
        if getTooken == tooken and len(all) == 4:
            newsSql = "select html_content from get_news where news_id = '" + news_id + "'"
            messageSql = "select * from news_comment where news_id = '" + news_id + "'"
            userBehaviorSql = "select is_comment,behavior_type from user_behavior where user_id = '" + user_id + "' and news_id = '" + news_id + "'"
            try:
                mSql.cur.execute(newsSql)
                # 提交到数据库执行,得到新闻内容
                news = mSql.cur.fetchall()
                news_content = news[0][0]
                #print(news_content)
                mSql.cur.execute(messageSql)
                # 提交到数据库执行,得到评论内容
                messageall = mSql.cur.fetchall()
                #print(messageall[0][1])
                if user_id:
                    mSql.cur.execute(userBehaviorSql)
                    # 提交到数据库执行,得到用户是否评论跟是否喜欢
                    userBehavior = mSql.cur.fetchall()
                    if userBehavior:

                        if userBehavior[0][0]:
                            is_comment = 0
                        else:
                            is_comment = userBehavior[0][0]
                        if userBehavior[0][1] == 2:
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
                            username = "select user.name,user_mess.image from user,user_mess where  user.user_id = '" + me[
                                0] + "' and " \
                                     "user_mess.user_id = '" + me[0] + "'"
                            mSql.cur.execute(username)
                            # 提交到数据库执行,得到评论的用户的信息
                            com_username = mSql.cur.fetchall()
                            head_url = com_username[0][1]
                            uname = com_username[0][0]
                            message.append({"head_url": head_url, "username": uname, "comment_time": times,"comment_content":comment_content,"dianzan_num":me[3]})

                data = {"content":news_content , "is_comment": is_comment, "is_love": is_love, "message": message}
                #print(data)
                print("data success!")
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                self.write(result)
                #****阅读相关数据库更新
                if user_id:
                    timescore = mSql.select_table(table = "user_behavior", column = "times,score", condition = "news_id", value = news_id + "' and user_id = '" + user_id)
                    #print("haha")
                    #print(timescore)
                    tag = mSql.select_table (table="get_news", column="tag", condition="news_id", value=news_id)

                    if timescore:
                        #******************************新闻分数******************************
                        #mSql.update_column(table = "user_behavior",column = "times",value_set = times, condition = "user_id",value_find = user_id + "' and news_id = '" +news_id)
                        uptimesSql = "update user_behavior set times  = times + 1 where user_id = '" +user_id+ "' and news_id = '" +news_id+ "'"
                        print(uptimesSql)
                        mSql.cur.execute (uptimesSql)
                        # 提交到数据库执行
                        mSql.cur.fetchall ()
                        mSql.conn.commit ()
                        upscoresSql = "update user_behavior set score  = score + 1 where user_id = '" + user_id + "' and news_id = '" + news_id + "'"
                        mSql.cur.execute (upscoresSql)
                        # 提交到数据库执行
                        mSql.cur.fetchall ()
                        mSql.conn.commit ()

                    else:
                        # ******************************新闻分数******************************
                        mSql.insert_table(table = "user_behavior", field = "(user_id,news_id,news_tag,score,times)", values = "('" +user_id+ "','" +news_id+ "','" +tag[0][0]+ "',1,1)")


                #设置老新闻
                is_old = "update get_news set is_old = 1 where news_id = '" + news_id+ "'"
                #print (is_old)
                mSql.cur.execute (is_old)
                # 提交到数据库执行
                mSql.cur.fetchall ()
                mSql.conn.commit ()

                # 设置新闻基本信息表阅读次数
                read_times = mSql.select_table(table = "news_mess", column = "read_times", condition = "news_id", value = news_id)
                if read_times:
                    readtimesSql = "update news_mess set read_times  = read_times + 1 where news_id = '" + news_id + "'"
                    print (readtimesSql)
                    mSql.cur.execute (readtimesSql)
                    # 提交到数据库执行
                    mSql.cur.fetchall ()
                    mSql.conn.commit ()

                else:
                    mSql.insert_table (table="news_mess", field="(news_id,tag,read_times)",
                                       values="('"  + news_id + "','" + tag [0] [0] + "',1)")


                #************************用户标签因子历史分数****************************
                if user_id:
                    if_exist = mSql.select_table (table="user_tag_score", column="user_id", condition="user_id", value=user_id)
                    tag_points = mSql.select_table (table="user_tag_score", column=tag [0] [0], condition="user_id", value=user_id)
                    if if_exist:
                        if tag_points:
                            if tag_points[0][0]:
                                point = "update user_tag_score set "+tag[0][0]+ " = " +tag[0][0]+ " + 1 where user_id = '" + user_id + "'"
                                print (point)
                                mSql.cur.execute (point)
                                # 提交到数据库执行
                                mSql.cur.fetchall ()
                                mSql.conn.commit ()
                            else:
                                point = "update user_tag_score set " + tag [0] [0] + " = 1 where user_id = '" + user_id + "'"
                                print (point)
                                mSql.cur.execute (point)
                                # 提交到数据库执行
                                mSql.cur.fetchall ()
                                mSql.conn.commit ()
                        else:
                            self.errorRequest (num=1)
                    else:
                        mSql.insert_table (table="user_tag_score", field="(user_id," +tag [0] [0]+ ")",
                                           values="('" + user_id + "',1)")


            except:
                # 出现错误则回滚
                mSql.conn.rollback()
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
            userSql = "select name,phone from user where user_id = '" + user_id + "'"
            userInfoSql = "select * from user_mess where user_id = '" + user_id + "'"
            love_timesSql = "select * from user_operate where user_id = '" + user_id + "'"
            readSql = "select times,is_comment from user_behavior where user_id = '" + user_id + "'"
            try:
                mSql.cur.execute (userSql)
                # 提交到数据库执行,得到用户电话
                user = mSql.cur.fetchall ()
                mSql.cur.execute (userInfoSql)
                # 提交到数据库执行,得到用户详情
                userInfo = mSql.cur.fetchall ()
                # 查询用户行为
                mSql.cur.execute (love_timesSql)
                love = mSql.cur.fetchall ()
                # 查询阅读
                mSql.cur.execute (readSql)
                allRead = mSql.cur.fetchall ()
                read_times = 0
                message_times = 0
                for each in allRead:
                    read_times = each [0]
                    if each [1] == 1:
                        message_times = message_times + 1
                data = {"user_name": user [0] [0], "phone": user [0] [1], "email": userInfo [0] [3],
                        "image": userInfo [0] [5],
                        "read_times": read_times, "love_times": len (love), "message_times": message_times}
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback ()

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
            userSql = "select name,phone from user where user_id = '" + user_id + "'"
            userInfoSql = "select * from user_mess where user_id = '" + user_id + "'"
            love_timesSql = "select * from user_operate where user_id = '" + user_id + "'"
            readSql = "select times,is_comment from user_behavior where user_id = '" + user_id + "'"
            try:
               mSql.update_column(table = "user",column = "name",value_set = user_name, condition  = "user_id",value_find = user_id)
               mSql.update_column (table="user_mess", column="email", value_set=email, condition="user_id",value_find=user_id)
               mSql.update_column (table="user_mess", column="image", value_set=image, condition="user_id",value_find=user_id)
               data=self.select(userSql,userInfoSql,love_timesSql,readSql)
               result = {"message": "success", "data": data}
               result = json.dumps (result)
               self.write (result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback ()
        else:
            self.errorRequest (num=0)

    def select(self,userSql,userInfoSql,love_timesSql,readSql):
        mSql.cur.execute (userSql)
        # 提交到数据库执行,得到用户电话
        user = mSql.cur.fetchall ()
        mSql.cur.execute (userInfoSql)
        # 提交到数据库执行,得到用户详情
        userInfo = mSql.cur.fetchall ()
        # 查询用户行为
        mSql.cur.execute (love_timesSql)
        love = mSql.cur.fetchall ()
        # 查询阅读
        mSql.cur.execute (readSql)
        allRead = mSql.cur.fetchall ()
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
        if getTooken == tooken and len (all) == 5:
            localtime = time.strftime ("%Y-%m-%d %H:%M:%S", time.localtime ())
            try:
                behavior_type = mSql.select_table(table = "user_behavior", column = "behavior_type", condition = "news_id", value = news_id + "' and user_id = '" +user_id)
                if behavior_type[0][0] == 1:
                    self.errorRequest (num=-1)
                else:
                    #用户喜欢
                    success = False
                    if is_love == '1':
                        tag = mSql.select_table(table = "get_news", column = "tag", condition = "news_id", value = news_id)
                        love_times = mSql.select_table(table = "news_mess", column = "love_times", condition = "news_id", value = news_id)
                        love_times = love_times[0][0] +1
                        tag_point = mSql.select_table(table = "user_tag_score", column = tag[0][0], condition = "user_id", value = user_id)
                        #is_userBehavior = mSql.select_table(table = "user_behavior", column = "*", condition = "news_id ", value = news_id + "' and user_id = '" +user_id)

                        #用户行为表的更新
                        update_love = mSql.update_column (table ="user_behavior" , column = "behavior_type",value_set = '1',condition = "news_id ", value_find = news_id + "' and user_id = '" +user_id )
                        #查询user _behavior表是否有该用户和新闻
                        is_operate = mSql.select_table(table = "user_operate", column = "*", condition = "news_id ", value = news_id + "' and user_id = '" +user_id)
                        #更新用户操作表
                        if is_operate:
                            operate_islove = mSql.update_column (table ="user_operate" , column = "is_love",value_set = '1',condition = "news_id ", value_find = news_id + "' and user_id = '" +user_id )
                            operate_time = mSql.update_column (table="user_operate", column="time", value_set=localtime,condition="news_id ",value_find=news_id + "' and user_id = '" + user_id)
                        else:
                            insert_operate = mSql.insert_table(table = "user_operate", field = "(user_id,news_id,is_love,time)", values = "('" +user_id+ "','" +news_id+ "','1','" +localtime+ "')")

                        #更新新闻基本信息表
                        update_mess = mSql.update_column (table ="news_mess" , column = "love_times",value_set = str(love_times),condition = "news_id ", value_find = news_id )

                        #********************更新用户标签因子分数（历史分数）******************************

                        point = "update user_tag_score set " + tag [0] [0] + " = " + tag [0] [0] + " + 1 where user_id = '" + user_id + "'"
                        print (point)
                        mSql.cur.execute (point)
                        # 提交到数据库执行
                        mSql.cur.fetchall ()
                        mSql.conn.commit ()

                        success = 1

                    #用户取消喜欢
                    elif is_love == '0':
                        tag = mSql.select_table (table="get_news", column="tag", condition="news_id", value=news_id)
                        love_times = mSql.select_table (table="news_mess", column="love_times", condition="news_id", value=news_id)
                        love_times = love_times [0] [0] + 1
                        tag_point = mSql.select_table (table="user_tag_score", column=tag [0] [0], condition="user_id",
                                                       value=user_id)
                        # 用户行为表的更新
                        update_love = mSql.update_column (table="user_behavior", column="behavior_type", value_set='0',
                                                  condition="news_id ", value_find=news_id + "' and user_id = '" + user_id)
                        # 更新用户操作表
                        operate_islove = mSql.update_column (table="user_operate", column="is_love", value_set='0',
                                                     condition="news_id ",value_find=news_id + "' and user_id = '" + user_id)
                        operate_time = mSql.update_column (table="user_operate", column="time", value_set="",
                                                   condition="news_id ", value_find=news_id + "' and user_id = '" + user_id)

                        # 更新新闻基本信息表
                        update_mess = mSql.update_column (table="news_mess", column="love_times", value_set="love_tomes - 1 ",
                                                    condition="news_id ", value_find=news_id)

                        # ********************更新用户标签因子分数（历史分数）******************************
                        user_tag_points = user_tag_points = mSql.update_column (table ="user_tag_score" , column = tag[0][0],value_set = tag[0][0] +" - 1",condition = "user_id ", value_find = user_id )
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
                mSql.conn.rollback ()

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
            timeTwo = int(each[2]) + 1
            times = each[0] + "-" + each[1] + "-" + "0" + str(timeTwo)
            try:
                love_listSql = "select news_id,time from user_operate where is_love = 1 " \
                               "and TIMESTAMPDIFF(DAY,time,'" +times+ "') < 7 and user_id = '" +user_id+ "'"
                #print(love_listSql)
                mSql.cur.execute (love_listSql)
                # 提交到数据库执行
                love_list = mSql.cur.fetchall ()
                data = []
                for item in love_list:
                    getNews = mSql.select_table(table = "get_news", column = "title,abstract,time", condition = "news_id", value = item[0])
                    each_get_news = getNews[0]
                    #news_
                    news_mess = mSql.select_table(table = "news_mess", column = "*", condition = "news_id", value = item[0])
                    image = mSql.select_table(table = "get_news", column = "image", condition = "news_id", value = item[0])
                    if image[0][0].count("http://") >1:
                        image = (image[0][0].split(","))[0]
                        #print(image)
                    else:
                        image = image[0][0]
                    if news_mess:
                        data.append({"news_id":news_mess[0][0],"tag":news_mess[0][1],"image":image,"read_times":news_mess[0][2],"love_times":news_mess[0][3],
                                     "comment_times":news_mess[0][4],"title":each_get_news[0],"abstract":each_get_news[1],"time":str(each_get_news[2])})
                #print(data)
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback ()

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
            self.loveList(hot_type,count,alrequest)

        else:
            self.errorRequest (num=0)

    def loveList(self,hot_type,count,alrequest):
        try:
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            startTime = (str(localtime).split(' '))[0]
            each = startTime.split('-')
            timeTwo = int(each[2]) + 1
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
            mSql.conn.rollback ()


    def love(self,time,count,alrequest):
        data = []
        #print("love")
        try:
            #allLove = mSql.select_table(table = "hot", column = "news_id,tag,love_times,read_times,comment_times", condition = "1", value = "1 order by love_times desc")
            listSql = "select news_id,tag,image,love_times,read_times,comment_times,abstract," \
                      "source,title from news_hot where TIMESTAMPDIFF(DAY,time,'" +time+ "') < 10 order by love_times desc"
            print(listSql)
            mSql.cur.execute (listSql)
            # 提交到数据库执行
            allLove = mSql.cur.fetchall ()
            for j in range (int (alrequest), int (alrequest) + int (count)):
                # print(self.dataNews (id_list[j][0]))
                love = allLove[j]
                if love[2].count ("http://") > 1:
                    image = (love[2].split (",")) [0]
                    # print(image)
                else:
                    image = love[2]
                data.append({"news_id":love[0],"tag":love[1],"image":image,"love_times":love[3],"read_times":love[4],"comment_times":love[5],"abstract":love[6],"source":love[7],"title":love[8]})

            result = {"message": "success", "data": data}
            result = json.dumps (result)
            self.write (result)
        except:
            self.errorRequest (num=0)
    def read(self,time,count,alrequest):
        data = []
        #print("read")
        try:
            # allLove = mSql.select_table(table = "hot", column = "news_id,tag,love_times,read_times,comment_times", condition = "1", value = "1 order by love_times desc")
            listSql = "select news_id,tag,image,love_times,read_times,comment_times,abstract," \
                      "source,title from news_hot where TIMESTAMPDIFF(DAY,time,'" + time + "') < 10 order by read_times desc"
            # print(listSql)
            mSql.cur.execute (listSql)
            # 提交到数据库执行
            allLove = mSql.cur.fetchall ()
            for j in range (int (alrequest), int (alrequest) + int (count)):
                # print(self.dataNews (id_list[j][0]))
                love = allLove [j]
                if love [2].count ("http://") > 1:
                    image = (love [2].split (",")) [0]
                    # print(image)
                else:
                    image = love [2]
                data.append ({"news_id": love [0], "tag": love [1],"image":image,"love_times":love[3],"read_times":love[4],
                              "comment_times":love[5],"abstract":love[6],"source":love[7],"title":love[8]})

            result = {"message": "success", "data": data}
            result = json.dumps (result)
            self.write (result)
        except:
            self.errorRequest (num=0)
    def comment(self,time,count,alrequest):
        data = []
        #print("commnet")
        try:
            # allLove = mSql.select_table(table = "hot", column = "news_id,tag,love_times,read_times,comment_times", condition = "1", value = "1 order by love_times desc")
            listSql = "select news_id,tag,image,love_times,read_times,comment_times,abstract," \
                      "source,title from news_hot where TIMESTAMPDIFF(DAY,time,'" + time + "') < 10 order by comment_times desc"
            # print(listSql)
            mSql.cur.execute (listSql)
            # 提交到数据库执行
            allLove = mSql.cur.fetchall ()
            for j in range (int (alrequest), int (alrequest) + int (count)):
                # print(self.dataNews (id_list[j][0]))
                love = allLove [j]
                if love [2].count ("http://") > 1:
                    image = (love [2].split (",")) [0]
                    # print(image)
                else:
                    image = love [2]
                data.append ({"news_id": love [0], "tag": love [1],"image":image,"love_times":love[3],"read_times":love[4],"comment_times":love[5],"abstract":love[6],"source":love[7],"title":love[8]})

            result = {"message": "success", "data": data}
            result = json.dumps (result)
            self.write (result)
        except:
            self.errorRequest (num=0)

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
            times = time.time()
            print(str(times))
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            try:

                mSql.insert_table(table = "news_feedback ", field = "(user_id,feedback,getTime)", values = "('" + user_id + "','" +feedBack+ "','"+ localtime +"')")
                data = {"flag": 1}
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback ()
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
            try:
                keySql = "select news_id from get_news where title like '%" +keyWord+ "%'"
                #print(keySql)
                mSql.cur.execute (keySql)
                # 提交到数据库执行
                news_id_list = mSql.cur.fetchall ()
                for news_id in news_id_list:
                    news_content = mSql.select_table (table="get_news",
                                                      column="news_id,title,time,source,image,abstract",
                                                      condition="news_id ", value=news_id[0])
                    opData = mSql.select_table (table="news_mess", column="read_times,love_times,comment_times",
                                                condition="news_id ", value=news_id[0])
                    if opData:
                        read_times = opData [0] [0]
                        love_times = opData [0] [1]
                        comment_times = opData [0] [2]
                    if news_content [0] [4].count ("http://") > 1:
                        image = (news_content [0] [4].split (",")) [0]
                        # print(image)
                    else:
                        image = news_content [0] [4]

                    data.append({"news_id": news_content [0][0], "title": news_content [0][1], "time": str(news_content[0][2]),
                                 "source": news_content [0] [3],"image": image, "abstract": news_content [0] [5], "read_times": read_times,
                                 "love_times": love_times, "comment_times": comment_times})
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                # print(data[0])
                self.write (result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback ()
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
        comment = user_id + "{++}" + content + "{++}" + localtime + "{++}" + '1' + "{##}"
        news_comment = news_id + "{++}" + content + "{++}" + localtime  + "{##}"
        if getTooken == tooken and len (all) == 5:
            try:
                tags = mSql.select_table(table = "get_news", column = "tag", condition = "news_id", value = news_id)
                tag = tags[0][0]
                is_comment = mSql.select_table(table = "news_comment", column = "comment", condition = "news_id", value = news_id)
                #print(is_comment)
                #如果该新闻已有评论
                if is_comment:
                    commentNew = is_comment[0][0] + comment
                    mSql.update_column(table = "news_comment",column = "comment",value_set = commentNew, condition = "news_id",value_find = news_id)
                #如果还没有评论
                else:
                    comment = user_id + "{++}" + content + "{++}" + localtime + "{++}" +'1' + "{##}"
                    mSql.insert_table(table = "news_comment", field = "(news_id,comment)", values = "('" + news_id + "','" + comment + "')")

                #****************************设置用户对应分数*******************************************
                upBehaviorSql = "update user_behavior set is_comment = 1,score = score + 2 " \
                                "where user_id = '" +user_id+ "' and news_id = '" +news_id+ "'"
                mSql.cur.execute (upBehaviorSql)
                mSql.conn.commit ()
                print ("评论成功，用户对此条新闻 分数 加1")

                #设置新闻基本信息表
                upNews_mess = "update news_mess set comment_times = comment_times + 1 where news_id = '"  + news_id + "'"
                mSql.cur.execute (upNews_mess)
                mSql.conn.commit ()
                print ("评论成功，用户对此条新闻 评论次数 加1")

                #设置用户操作表
                is_comment = mSql.select_table(table = "user_operate", column = "comment", condition = "user_id", value = user_id +"' and news_id = '" +news_id)
                if is_comment:
                    mSql.update_column(table = "user_operate",column = "comment",value_set = is_comment[0][0] + news_comment, condition = "user_id",value_find = user_id + "' and news_id = '" + news_id)
                else:
                    mSql.insert_table(table = "user_operate", field = "(user_id,news_id,comment,is_love,time)",
                                      values = "('" +user_id+ "','" +news_id+ "','" +news_comment+ "',0,'" +localtime +"')")
                print("评论成功，用户操作表更新")

                #*******************用户标签因子分数表对应该标签历史分数***************************
                point = "update user_tag_score set " + tag + " = " + tag  + " + 2 where user_id = '" + user_id + "'"
                #print (point)
                mSql.cur.execute (point)
                # 提交到数据库执行,得到评论内容
                mSql.cur.fetchall ()
                mSql.conn.commit ()
                print("评论成功，用户对标签因子 分数 加2")


                #查询评论的用户的个人信息返回
                image = mSql.select_table(table = "user_mess", column = "image", condition = "user_id", value = user_id)
                name = mSql.select_table (table="user", column="name", condition="user_id", value=user_id)
                data = {"user_id": user_id,"user_name":name[0][0],"user_image":image[0][0],"news_id":news_id,
                        "content":content,"comment_time":localtime}
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback ()
        else:
            self.errorRequest (num=0)

class LoveComment(Confirm):
    # 反馈
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
            try:
                commentAllList = mSql.select_table(table = "news_comment", column = "*", condition = "news_id", value = news_id)
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
                mSql.update_column(table = "news_comment",column = "comment",value_set = news_comment, condition = "news_id",value_find = news_id)
                data = {"flag": 1}
                result = {"message": "success", "data": data}
                result = json.dumps (result)
                self.write (result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback ()
        else:
            self.errorRequest (num=0)


