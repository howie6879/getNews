#-*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
from handlers.base import BaseHandler

class Spider(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        header = "爬虫管理"
        self.render("spider.html",header=header)