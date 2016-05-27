# -*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
import hashlib
import methods.db as m_sql
from config.n_conf import admin
from handlers.base import BaseHandler


class ChangePass(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        password = self.get_argument("pass")
        password = str(hashlib.md5((admin["TOKEN"] + password).encode("utf-8")).hexdigest())
        sql = "update n_admin set pass='" + password + "' where name = 'admin'"  # 执行SQL语句
        m_sql.cur.execute(sql)
        # 提交到数据库执行
        m_sql.conn.commit()
        self.write("密码修改成功")

