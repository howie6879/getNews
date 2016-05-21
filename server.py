#-*- coding: utf-8 -*
__author__ = 'Howie'

import tornado.options
import tornado.ioloop
from application import  application


def main():
    tornado.options.parse_command_line()
    application.listen(8888)
    print("Development server is running at http://127.0.0.1:8888")
    print("Quit the server with Control-C")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()