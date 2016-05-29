#-*- coding: utf-8 -*
__author__ = 'Howie'

import tornado.web

class ErrorHandler(tornado.web.RequestHandler):

    def write_error(self, status_code, **kwargs):
        self.write("错误状态码{0}.\n".format(
            status_code))