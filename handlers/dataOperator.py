#-*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
import time
import methods.db as m_sql
from handlers.base import BaseHandler
from spider import allSpider
from controller.dataController import DataController,newSource

class DataOperator(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        #allSpider.touTiao(category=allSpider.ts.category, page=2, num=20, time=time.time())
        #allSpider.sina()
        #allSpider.merge()
        #allSpider.wordAna()
        #print(DataController.repeatedData(['wordAna','allNews']))      #进行去重操作
        DataController.rmAllNews(newSource)
        #DataController.rmRepeate(['wordAna','wordAnaNews'])            #删除分词文件夹里面的表


    def getTimestamp(startTime):
        """
        Des:    将时间转化为时间戳
        param:  startTime="2016-05-17 12:00:00"(格式)
        return: timeStamp
        """
        timeArray = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp