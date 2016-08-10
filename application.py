#-*- coding: utf-8 -*
__author__ = 'Howie'
import tornado.web
import os
from handlers.errorHandler import ErrorHandler
from handlers.index import IndexHandler
from handlers.admin import AdminHandler
from handlers.dataAna import DataAna
from handlers.spider import Spider
from handlers.system import System
from handlers.newsManage import NewsManage
from handlers.UmFeedBack import UmFeedBack
from handlers.UmMyNote import UmMyNote
from handlers.userManage import UserManage
from handlers.changePass import ChangePass
from handlers.dataOperator import DataOperator
import handlers.api.newsApi as api

url = [
    (r'/', IndexHandler),
    (r'/admin',AdminHandler),
    (r'/dataAna',DataAna),
    (r'/spider', Spider),
    (r'/system',System),
    (r'/newsManage',NewsManage),
    (r'/userManage',UserManage),
    (r'/umMyNote', UmMyNote),
    (r'/umFeedBack', UmFeedBack),
    (r'/changePass',ChangePass),
    (r'/dataOperator',DataOperator),
    (r'/api/register',api.Register),
    (r'/api/login', api.Login),
    (r'/api/newstags', api.NewsTags),
    (r'/api/newscontent', api.NewsContent),
    (r'/api/userinfo', api.UserInfo),
    (r'/api/userinfochange', api.UserInfoChange),
    (r'/api/lovenews', api.LoveNews),
    (r'/api/lovelist', api.LoveList),
    (r'/api/hotlist', api.HotList),
    (r'/api/feedback', api.FeedBack),
    (r'/api/keyword', api.KeyWord),
    (r'/api/comment', api.Comment),
    (r'/api/lovecomment', api.LoveComment),
    (r'/api/exitread', api.ExitRead),
    (r'/api/adminuser', api.AdminUser),
    (r'/api/adminuserinfo', api.AdminUserInfo),
    (r'/api/adminfeedback', api.AdminFeedback),
    (r'/api/returntags', api.ReturnTags),
    #这个页面处理语句必须放在最后
    (r".*", ErrorHandler)
]

setting = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret = "XQ5rhITaQ1m7HoN40CcggWPCvR2jqUn1tY9E3kWU+yc=",
    #xsrf_cookies = True,
    debug = True,
    login_url = '/',
)

application = tornado.web.Application(
    handlers = url,
    **setting
)