#-*-coding:utf-8-*-
__author__ = 'howie'
import base64
import uuid

cookie_secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
#print(cookie_secret)