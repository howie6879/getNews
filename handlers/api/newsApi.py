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
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        if getTooken == tooken and len(all) == 5:
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
                    if insertSql and user_messSql:
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
            recommend = "select * from news_recommend where user_id = " + user_id
            try:
                mSql.cur.execute(recommend)
                # 提交到数据库执行
                information = mSql.cur.fetchall()
                # 得到该用户的推荐新闻
                news = information[0][1].split('#')
                # print(int(alrequest)+int(count))
                if int(alrequest) + int(count) > len(news):
                    # 请求大于有效值
                    self.errorRequest(num=-1)
                else:
                    for i in range(int(alrequest), int(alrequest) + int(count)):
                        news_id = news[i].split('+')[0]
                        # 如果tag为空，则默认全部的推荐
                        if tag == '':
                            newsl = "select get_news.news_id,get_news.title,get_news.time,get_news.source," \
                                    "get_news.image,get_news.abstract,news_mess.read_times,news_mess.love_times," \
                                    "news_mess.comment_times from get_news,news_mess where get_news.news_id" \
                                    " = '" + news_id + "' and news_mess.news_id ='" + news_id + "'"
                        else:
                            newsl = "select get_news.news_id,get_news.title,get_news.time,get_news.source," \
                                    "get_news.image,get_news.abstract,news_mess.read_times,news_mess.love_times," \
                                    "news_mess.comment_times from get_news,news_mess where get_news.news_id" \
                                    " = '" + news_id + "' and get_news.tag = '" + tag + "' and news_mess.news_id " \
                                                                                        "='" + news_id + "' and news_mess.tag = '" + tag + "'"
                        mSql.cur.execute(newsl)
                        # 提交到数据库执行
                        new_list = mSql.cur.fetchall()
                        for each in new_list:
                            data.append(
                                {'news_id': each[0], 'title': each[1], 'time': "2016-06-02 21:13:48", 'source': each[3],
                                 'image': each[4], 'abstract': each[5], 'read_times': each[6],
                                 'love_times': each[7], 'comment_times': each[8]})
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                self.write(result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback()
        else:
            self.errorRequest(num=0)


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
        if getTooken == tooken and len(all) == 4:
            newsSql = "select html_content from get_news where news_id = '" + news_id + "'"
            messageSql = "select * from news_comment where news_id = '" + news_id + "'"
            userBehaviorSql = "select is_comment,behavior_type from user_behavior where user_id = '" + user_id + "' and news_id = '" + news_id + "'"
            try:
                mSql.cur.execute(newsSql)
                # 提交到数据库执行,得到新闻内容
                news = mSql.cur.fetchall()
                mSql.cur.execute(messageSql)
                # 提交到数据库执行,得到评论内容
                messageall = mSql.cur.fetchall()
                mSql.cur.execute(userBehaviorSql)
                # 提交到数据库执行,得到用户是否评论跟是否喜欢
                userBehavior = mSql.cur.fetchall()
                if userBehavior[0][1] == 2:
                    is_love = 1
                else:
                    is_love = 0
                # {##}每条新闻详情
                for mess in messageall[0][1].split("{##}"):
                    me = mess.split("{++}")
                    # 通过用户编号查询用户评论的昵称和头像
                    username = "select user.name,user_mess.image from user,user_mess where  user.user_id = '" + me[
                        0] + "' and " \
                             "user_mess.user_id = '" + me[0] + "'"
                    mSql.cur.execute(username)
                    # 提交到数据库执行,得到评论的用户的信息
                    com_username = mSql.cur.fetchall()
                    message.append({"head_url": com_username[0][1], "username": com_username[0][0], "time": me[2],
                                    "comment_content": me[1]})
                data = {"content": news[0][0], "is_comment": userBehavior[0][0], "is_love": is_love, "message": message}
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                self.write(result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback()
        else:
            self.errorRequest(num=0)


class UserInfo(Confirm):
    # 返回用户信息
    def get(self, *args, **kwargs):
        all = self.request.arguments
        user_id = self.get_argument('userid')
        getTooken = self.get_argument('tooken')
        time = self.get_argument('time')
        tooken = self.tooken(time=time)
        message = []
        if getTooken == tooken and len(all) == 3:
            userSql = "select name,phone from user where user_id = '" + user_id + "'"
            userInfoSql = "select * from user_mess where user_id = '" + user_id + "'"
            try:
                mSql.cur.execute(userSql)
                # 提交到数据库执行,得到用户电话
                user = mSql.cur.fetchall()
                mSql.cur.execute(userInfoSql)
                # 提交到数据库执行,得到用户详情
                userInfo = mSql.cur.fetchall()
                data = {"user_name": user[0][0], "phone": user[0][1], "sex": userInfo[0][1],
                        "age": userInfo[0][2], "email": userInfo[0][3], "address": userInfo[0][4],
                        "image": userInfo[0][5]}
                result = {"message": "success", "data": data}
                result = json.dumps(result)
                print(data)
                self.write(result)
            except:
                # 出现错误则回滚
                mSql.conn.rollback()
        else:
            self.errorRequest(num=0)
