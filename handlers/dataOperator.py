# -*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
import time
import methods.db as m_sql
from handlers.base import BaseHandler
from spider import allSpider
from controller.dataController import DataController, newsSource
from spider.newsDb.insertNews import newsInsert


class DataOperator(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # 新闻种类
        action = self.get_argument('action')
        if action == "getNews":
            page = int(self.get_argument('page'))
            num = int(self.get_argument('num'))
            a = ["news_fashion", "news_regimen", "news_story", "news_discovery", "news_essay", "news_food"]
            cate = ["news_society", "news_entertainment",
                    "news_tech", "news_car", "news_sports", "news_finance", "news_military", "news_world",
                    "news_fashion", "news_travel", "news_discovery", "news_baby", "news_regimen", "news_story",
                    "news_essay", "news_game", "news_history", "news_food"]
            allSpider.touTiao(category=cate, page=page, num=num)
            allSpider.sina(num=1000, page=2)
        elif action == "repeatedData":
            # 先进行合并
            allSpider.merge()
            # 进行去重
            print(DataController.repeatedData(['wordAna', 'allNews']))
        elif action == "anaData":
            # 进行词性分析
            allSpider.wordAna()
        elif action == "rmAllNews":
            DataController.rmAllNews(newsSource)
        elif action == "insertDB":
            # 将新闻插入数据库
            newsInsert.insertSql("wordAnaNews")
            # 删除分词文件夹里面的表
            DataController.rmRepeate(['wordAna', 'wordAnaNews'])
            print("success")
