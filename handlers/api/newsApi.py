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
                    loveTageSql = mSql.insert_table(table="user_love_tag", field="(user_id,tags)",
                                                    values="('" + str(user_id) + "','" + tags + "')")
                    if insertSql and user_messSql and loveTageSql:
                        data = {"flag": 1}
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
                if information:
                    if information[0][3] == passwd:
                        # 登录成功
                        data = {"flag": 1}
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
                    mSql.cur.execute(recommend)
                    # 提交到数据库执行
                    information = mSql.cur.fetchall()
                    # 得到该用户的推荐新闻
                    news = information[0][1].split('#')
                    lenght = len(news)
                    news_id = ''
                    print(lenght)
                    if int(alrequest) + int(count) > len(news):
                        # 请求大于有效值
                        self.errorRequest(num=-1)
                    else:
                        if tag == '':
                            for i in range(int(alrequest), int(alrequest) + int(count)):
                                news_id = news[i].split('+')[0]
                                data.append(self.returnData(news_id))
                        else:
                            n = 0
                            for i in range(int(alrequest), lenght):
                                if n < int(count):
                                    news_id = news[i].split('+')[0]
                                    if tag == news[i].split('+')[1]:
                                        n = n + 1
                                        data.append(self.returnData(news_id))
                                    else:
                                        continue
                else:
                    if tag:
                        id_listSql = "select news_id from get_news where tag = '" + tag + "'"
                        mSql.cur.execute(id_listSql)
                        # 提交到数据库执行
                        id_list = mSql.cur.fetchall()
                    else:
                        id_listSql = "select news_id from get_news"
                        mSql.cur.execute(id_listSql)
                        # 提交到数据库执行
                        id_list = mSql.cur.fetchall()
                    for j in range(int(alrequest), int(alrequest) + int(count)):
                        data.append(self.data(id_list[j][0]))
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                self.write(result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback()
        else:
            self.errorRequest(num=0)

    def returnData(self, news_id):
        data = []
        newsl = "select get_news.news_id,get_news.title,get_news.time,get_news.source," \
                "get_news.image,get_news.abstract,news_mess.read_times,news_mess.love_times," \
                "news_mess.comment_times from get_news,news_mess where get_news.news_id" \
                " = '" + news_id + "' and news_mess.news_id ='" + news_id + "'"
        mSql.cur.execute(newsl)
        # 提交到数据库执行
        new_list = mSql.cur.fetchall()
        for each in new_list:
            # print(str(each[2]))
            # dateC = str(each[2])
            # timestamp = time.mktime (dateC)
            # print(timestamp)
            print(each[2])
            data.append(
                {'news_id': each[0], 'title': each[1], 'time': "2016-06-02 21:13:48", 'source': each[3],
                 'image': each[4], 'abstract': each[5], 'read_times': each[6],
                 'love_times': each[7], 'comment_times': each[8]})
            # print(data)
            return data

    def data(self, news_id):
        read_times = 0
        love_times = 0
        comment_times = 0
        news_content = mSql.select_table(table="get_news", column="news_id,title,time,source,image,abstract",
                                         condition="news_id ", value=news_id)
        opData = mSql.select_table(table="news_mess", column="read_times,love_times,comment_times",
                                   condition="news_id ", value=news_id)
        if opData:
            read_times = opData[0][0]
            love_times = opData[0][1]
            comment_times = opData[0][2]
        if news_content[0][4].count("http://") > 1:
            image = (news_content[0][4].split(","))[0]
            print(image)
        else:
            image = news_content[0][4]
        # print(str(news_content[0][2]))
        # print(str(news_content))
        data = {'news_id': news_content[0][0], 'title': news_content[0][1], 'time': str(news_content[0][2]),
                'source': news_content[0][3],
                'image': image, 'abstract': news_content[0][5], 'read_times': read_times,
                'love_times': love_times, 'comment_times': comment_times}
        # print(data)
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
                print(news_content)
                mSql.cur.execute(messageSql)
                # 提交到数据库执行,得到评论内容
                messageall = mSql.cur.fetchall()
                if user_id:
                    mSql.cur.execute(userBehaviorSql)
                    # 提交到数据库执行,得到用户是否评论跟是否喜欢
                    userBehavior = mSql.cur.fetchall()
                    if userBehavior:
                        is_comment = userBehavior[0][0]
                        if userBehavior[0][1] == 2:
                            is_love = 1
                        else:
                            is_love = 0
                # {##}每条新闻详情
                if messageall:
                    for mess in messageall[0][1].split("{##}"):
                        me = mess.split("{++}")
                        time = str(me[2])
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
                    message.append({"head_url": head_url, "username": uname, "time": time,
                                    "comment_content": comment_content})
                data = {"content": news_content, "is_comment": is_comment, "is_love": is_love, "message": message}
                print(data)
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                self.write(result)
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
                mSql.cur.execute(userSql)
                # 提交到数据库执行,得到用户电话
                user = mSql.cur.fetchall()
                mSql.cur.execute(userInfoSql)
                # 提交到数据库执行,得到用户详情
                userInfo = mSql.cur.fetchall()
                # 查询用户行为
                mSql.cur.execute(love_timesSql)
                love = mSql.cur.fetchall()
                # 查询阅读
                mSql.cur.execute(readSql)
                allRead = mSql.cur.fetchall()
                read_times = 0
                message_times = 0
                for each in allRead:
                    read_times = each[0]
                    if each[1] == 1:
                        message_times = message_times + 1
                data = {"user_name": user[0][0], "phone": user[0][1], "email": userInfo[0][3],
                        "image": userInfo[0][5],
                        "read_times": read_times, "love_times": len(love), "message_times": message_times}
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                self.write(result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback()

            else:
                self.errorRequest(num=0)


class UserInfoChange(Confirm):
    # 用户更改个人信息
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument('userid')
        user_name = self.get_argument('username')
        image = self.get_argument('image')
        email = self.get_argument('email')
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        if getTooken == tooken and len(all) == 6:
            userSql = "select name,phone from user where user_id = '" + user_id + "'"
            userInfoSql = "select * from user_mess where user_id = '" + user_id + "'"
            love_timesSql = "select * from user_operate where user_id = '" + user_id + "'"
            readSql = "select times,is_comment from user_behavior where user_id = '" + user_id + "'"
            try:
                mSql.update_column(table="user", column="name", value_set=user_name, condition="user_id",
                                   value_find=user_id)
                mSql.update_column(table="user_mess", column="email", value_set=email, condition="user_id",
                                   value_find=user_id)
                mSql.update_column(table="user_mess", column="image", value_set=image, condition="user_id",
                                   value_find=user_id)
                data = self.select(userSql, userInfoSql, love_timesSql, readSql)
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                self.write(result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback()
        else:
            self.errorRequest(num=0)

    def select(self, userSql, userInfoSql, love_timesSql, readSql):
        mSql.cur.execute(userSql)
        # 提交到数据库执行,得到用户电话
        user = mSql.cur.fetchall()
        mSql.cur.execute(userInfoSql)
        # 提交到数据库执行,得到用户详情
        userInfo = mSql.cur.fetchall()
        # 查询用户行为
        mSql.cur.execute(love_timesSql)
        love = mSql.cur.fetchall()
        # 查询阅读
        mSql.cur.execute(readSql)
        allRead = mSql.cur.fetchall()
        read_times = 0
        message_times = 0
        for each in allRead:
            read_times = each[0]
            if each[1] == 1:
                message_times = message_times + 1
        data = {"user_name": user[0][0], "phone": user[0][1], "email": userInfo[0][3],
                "image": userInfo[0][5],
                "read_times": read_times, "love_times": len(love), "message_times": message_times}
        return data


class LoveNews(Confirm):
    # 喜欢功能
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument('userid')
        is_love = self.get_argument('islove')
        news_id = self.get_argument('newsid')
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        if getTooken == tooken and len(all) == 5:
            try:
                if is_love == '1':
                    tag = mSql.select_table(table="get_news", column="tag", condition="news_id", value=news_id)
                    love_times = mSql.select_table(table="news_mess", column="love_times", condition="news_id",
                                                   value=news_id)
                    love_times = love_times[0][0] + 1
                    tag_point = mSql.select_table(table="user_tag_score", column=tag[0][0], condition="user_id",
                                                  value=user_id)
                    # is_userBehavior = mSql.select_table(table = "user_behavior", column = "*", condition = "news_id ", value = news_id + "' and user_id = '" +user_id)

                    # 用户行为表的更新
                    update_love = mSql.update_column(table="user_behavior", column="behavior_type", value_set='1',
                                                     condition="news_id ",
                                                     value_find=news_id + "' and user_id = '" + user_id)
                    # 查询user _behavior表是否有该用户和新闻
                    is_operate = mSql.select_table(table="user_operate", column="*", condition="news_id ",
                                                   value=news_id + "' and user_id = '" + user_id)
                    # 更新用户操作表
                    if is_operate:
                        operate_islove = mSql.update_column(table="user_operate", column="is_love", value_set='1',
                                                            condition="news_id ",
                                                            value_find=news_id + "' and user_id = '" + user_id)
                        operate_time = mSql.update_column(table="user_operate", column="time", value_set=time,
                                                          condition="news_id ",
                                                          value_find=news_id + "' and user_id = '" + user_id)
                    else:
                        insert_operate = mSql.insert_table(table="user_operate", field="(user_id,news_id,is_love,time)",
                                                           values="('" + user_id + "','" + news_id + "','1','" + time + "')")
                    # 更新新闻基本信息表
                    update_mess = mSql.update_column(table="news_mess", column="love_times", value_set=str(love_times),
                                                     condition="news_id ", value_find=news_id)
                    # ********************更新用户标签因子分数（历史分数）******************************
                    print(tag_point)
                    if tag_point:
                        point = tag_point[0][0] + 1
                        user_tag_points = mSql.update_column(table="user_tag_score", column=tag[0][0],
                                                             value_set=str(point), condition="user_id ",
                                                             value_find=user_id)
                    else:
                        point = 1
                        insert_tage_score = mSql.insert_table(table="user_tag_score",
                                                              field="(user_id," + tag[0][0] + ")",
                                                              values="('" + user_id + "','" + str(point) + "')")
            except:
                # 出现错误则回滚
                mSql.conn.rollback()

        else:
            self.errorRequest(num=0)


class LoveList(Confirm):
    # 查询返回用户历史喜欢新闻列表
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument('userid')
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        if getTooken == tooken and len(all) == 3:
            try:
                love_listSql = "select news_id,time from user_operate where is_love = 1 " \
                               "and now()-time < 7*24*3600 and user_id = '" + user_id + "'"
                # print(love_listSql)
                mSql.cur.execute(love_listSql)
                # 提交到数据库执行
                love_list = mSql.cur.fetchall()
                data = []
                for item in love_list:
                    news_mess = mSql.select_table(table="news_mess", column="*", condition="news_id", value=item[0])
                    image = mSql.select_table(table="get_news", column="image", condition="news_id", value=item[0])
                    if image[0][0].count("http://") > 1:
                        image = (image[0][0].split(","))[0]
                        print(image)
                    else:
                        image = image[0][0]
                    if news_mess:
                        data.append({"user_id": news_mess[0][0], "tag": news_mess[0][1], "image": image,
                                     "read_times": news_mess[0][2], "love_times": news_mess[0][3],
                                     "comment_times": news_mess[0][4]})
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                self.write(result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback()

        else:
            self.errorRequest(num=0)


class HotList(Confirm):
    # 查询返回热点新闻
    def get(self, *args, **kwargs):
        all = self.request.arguments
        hot_type = self.get_argument('hot')
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        if getTooken == tooken and len(all) == 3:
            if hot_type == 1:
                self.loveList(hot_type)
            elif hot_type == 2:
                pass
            elif hot_type == 3:
                pass
        else:
            self.errorRequest(num=0)

    def loveList(self, hot_type):
        pass
