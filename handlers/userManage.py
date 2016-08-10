#-*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
from handlers.base import BaseHandler

class UserManage(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        header = "用户管理"

        self.render("userManage.html",header=header)