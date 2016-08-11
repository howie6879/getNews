# -*-coding:utf-8-*-
__author__ = 'howie'
import tornado.web
import tornado.escape
from handlers.base import BaseHandler
from spider import allSpider
from controller.dataController import DataController, newsSource
from spider.newsDb.insertNews import newsInsert
from system.classPredict.main import startPredict
from system.latentFactor.geneCalcul import GeneCulcal
from methods.pDb import newsDb


class DataOperator(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # 新闻种类
        action = self.get_argument('action')
        if action == "getNews":
            page = int(self.get_argument('page'))
            num = int(self.get_argument('num'))
            cate = ["news_society", "news_entertainment",
                    "news_tech", "news_car", "news_sports", "news_finance", "news_military", "news_world",
                    "news_fashion", "news_travel", "news_discovery", "news_baby", "news_regimen", "news_story",
                    "news_essay", "news_game", "news_history", "news_food"]
            allSpider.touTiao(category=cate, page=page, num=num)
            allSpider.sina(num=1000, page=10)
            print("success")
        elif action == "repeatedData":
            # 先进行合并
            allSpider.merge()
            # 进行去重
            print(DataController.repeatedData(['wordAna', 'allNews']))
            print("success")
        elif action == "anaData":
            # 进行词性分析
            allSpider.wordAna()

        elif action == "rmAllNews":
            DataController.rmAllNews(newsSource)
            print("success")
        elif action == "insertDB":
            # 清除老数据
            db = newsDb()
            db.exeSql("delete from news_tag_deep")
            db.exeSql("delete from news_nums")
            db.exeSql("delete from get_news where is_old=0")
            db.exeSql("insert into news_nums select * from news_nums_view")
            # 将新闻插入数据库
            newsInsert.insertSql("wordAnaNews")
            # 删除分词文件夹里面的表
            DataController.rmRepeate(['wordAna', 'wordAnaNews'])
            startPredict()
            gc = GeneCulcal()
            gc.getMatData()
            print("success")
