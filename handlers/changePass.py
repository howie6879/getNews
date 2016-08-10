# -*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
import hashlib
from methods.pDb import newsDb
from config.n_conf import admin
from handlers.base import BaseHandler


class ChangePass(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        password = self.get_argument("pass")
        password = str(hashlib.md5((admin["TOKEN"] + password).encode("utf-8")).hexdigest())
        sql = "update n_admin set pass='" + password + "' where name = 'admin'"  # 执行SQL语句
        mSql = newsDb()
        if mSql.exeSql(sql):
            self.write("密码修改成功")
        else:
            self.write("密码修改失败")
