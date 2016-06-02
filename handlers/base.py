#-*- coding: utf-8 -*
__author__ = 'Howie'

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")
    def write_error(self, status_code, **kwargs):
        self.write("错误页面,状态码{0}.\n".format(
            status_code))