#-*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
from handlers.base import BaseHandler

class UmFeedBack(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):


        self.render("umFeedBack.html")