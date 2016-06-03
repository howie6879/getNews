# -*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
import time
import methods.db as m_sql
from handlers.base import BaseHandler
from spider import allSpider
from controller.dataController import DataController, newSource


class DataOperator(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # 新闻种类
        category = ["news_sports", "news_finance","news_military", "news_world",
            "news_fashion", "news_travel", "news_discovery", "news_baby", "news_regimen", "news_story",
            "news_essay", "news_game", "news_history", "news_food"]

        #allSpider.touTiao(category=category, page=2000, num=20)
        #allSpider.sina(num=1000, page=400)
        #allSpider.merge()
        #print(DataController.repeatedData(['wordAna','allNews']))      #进行去重操作
        # allSpider.wordAna()

        DataController.rmAllNews(newSource)
        # DataController.rmRepeate(['wordAna','allNews'])            #删除去重文件夹里面的表
        # DataController.rmRepeate(['wordAna','wordAnaNews'])            #删除分词文件夹里面的表

    def getTimestamp(startTime):
        """
        Des:    将时间转化为时间戳
        param:  startTime="2016-05-17 12:00:00"(格式)
        return: timeStamp
        """
        timeArray = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
