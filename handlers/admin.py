# -*- coding: utf-8 -*
__author__ = 'Howie'

import tornado.web
import tornado.escape
from methods.pDb import newsDb
from handlers.base import BaseHandler


class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user = self.get_argument("user")
        if user == "logout":
            self.clear_cookie("user")
            self.render("index.html")
        else:
            header = "新闻推荐系统后台"
            cateType = {"news_society":"社会", "news_entertainment":"娱乐","news_tech":"科技", "news_car":"汽车", "news_sports":"体育", "news_finance":"财经",
                    "news_military":"军事", "news_world":"国际","news_fashion":"时尚", "news_travel":"旅游", "news_discovery":"探索", "news_baby":"育儿",
                    "news_regimen":"养生", "news_story":"故事","news_essay":"美文", "news_game":"游戏", "news_history":"历史", "news_food":"美食"}
            numTag = {}
            for i in cateType.keys():
                mSql = newsDb()
                result = mSql.select_table(table="news_nums",column="nums",condition="tag",value=i)
                numTag[cateType[i]]=result[0][0]
            #排序
            sortTag = list(sorted(numTag.items(), key=lambda d:d[1], reverse = True))
            self.render("admin.html", header=header, numTag=numTag,sortTag=sortTag[0:7])
