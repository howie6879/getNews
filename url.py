#-*- coding: utf-8 -*
__author__ = 'Howie'

"""
the url structure of website
"""

from handlers.index import IndexHandler
from handlers.admin import AdminHandler

url = [
    (r'/', IndexHandler),
    (r'/admin',AdminHandler)
]