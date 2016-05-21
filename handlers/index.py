#-*- coding: utf-8 -*
__author__ = 'Howie'

import tornado.escape
import hashlib
import methods.db as m_sql
from config.n_conf import admin
from handlers.base import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html") if admin["WEBSITE"] else self.write("<h3>网站正在维护...</h3>")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        result = m_sql.select_table("n_admin", "*", "name", username)
        if result:
            db_pwd = result[0][2]
            password = hashlib.md5((admin["TOKEN"]+password).encode("utf-8")).hexdigest()
            if db_pwd == password:
                self.set_current_user(username)     #将当前用户名写入cookie
                self.write(username)
            else:
                self.clear_cookie("user")
                self.write("-1")
        else:
            self.clear_cookie("user")
            self.write("-1")

    def set_current_user(self,user):
        if user:
            self.set_secure_cookie('user',tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")
