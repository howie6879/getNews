#-*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
import methods.db as m_sql
from handlers.base import BaseHandler

class NewsManage(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        header = "新闻管理"
        self.render("newsManage.html",header=header)