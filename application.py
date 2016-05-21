#-*- coding: utf-8 -*
__author__ = 'Howie'
import tornado.web
import os
from handlers.index import IndexHandler
from handlers.admin import AdminHandler

url = [
    (r'/', IndexHandler),
    (r'/admin',AdminHandler)
]

setting = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    #xsrf_cookies = True,
    debug = True,
    login_url = '/',
)

application = tornado.web.Application(
    handlers = url,
    **setting
)