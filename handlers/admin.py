#-*- coding: utf-8 -*
__author__ = 'Howie'

import tornado.web
import tornado.escape
import methods.db as m_sql
from handlers.base import BaseHandler

class AdminHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user = self.get_argument("user")
        if user=="logout":
            self.clear_cookie("user")
            self.render("index.html")
        else:
            username = tornado.escape.json_decode(self.current_user)
            header = "新闻推荐系统后台"
            result = m_sql.select_table("n_admin", "*", "name", username)
            self.render("admin.html",header=header)