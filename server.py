# -*- coding: utf-8 -*
__author__ = 'Howie'

import tornado.options
import tornado.ioloop
from application import application


def main(port):
    #tornado.options.parse_command_line()
    application.listen(port)
    print("Development server is running at http://127.0.0.1:%s" % port)
    print("Quit the server with Control-C")
    tornado.ioloop.IOLoop.instance().start()

#main(8888)