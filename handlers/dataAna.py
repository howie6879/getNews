#-*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
from handlers.base import BaseHandler

class DataAna(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        header = "数据分析"
        self.render("dataAna.html",header=header)