#-*- coding: utf-8 -*
__author__ = 'Howie'

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")