#-*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
from handlers.base import BaseHandler

class System(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        header = "系统信息"
        self.render("system.html",header=header)