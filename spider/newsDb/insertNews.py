# -*- coding: utf-8 -*
__author__ = 'Jeezy'

import os
import time
import hashlib
from methods.pDb import newsDb
import random
import pandas as pd



class newsInsert:
    def __init__(self):
        pass

    def insertSql(self, mainPath):
        path = os.path.abspath('.') + "/spider/wordAna/" + mainPath
        for dir in os.listdir(path):
            if os.path.splitext(dir)[1] == ".xlsx":
                file = os.path.join(path, dir)
                self.insert(file)

    def insert(self, file):
        try:
            data = pd.read_excel(file,sheetname="allNews")
            data = data.drop_duplicates(subset='title', keep='last')
            db = newsDb()
            cateType = {"news_society": "社会", "news_entertainment": "娱乐", "news_tech": "科技", "news_car": "汽车",
                        "news_sports": "体育", "news_finance": "财经",
                        "news_military": "军事", "news_world": "国际", "news_fashion": "时尚", "news_travel": "旅游",
                        "news_discovery": "探索", "news_baby": "育儿",
                        "news_regimen": "养生", "news_story": "故事", "news_essay": "美文", "news_game": "游戏",
                        "news_history": "历史", "news_food": "美食"}
            tag = file.split('&')[1]
            for i in range(0, len(data) ):
                value = data.values[i]
                if value[8] in cateType.keys(): tag = value[8]
                if value[11]:
                    times = time.time()
                    md5newid = hashlib.md5(str(times).encode("utf-8")).hexdigest()
                    startNum = random.randint(0, (len(md5newid) - 20))
                    newsId = str(md5newid)[startNum:(startNum + 20)]
                    try:
                        mysqlSuccess = db.insert_table(table="get_news", field="(news_id,news_link,source,title,abstract,tag,"
                                                                                 "text_content,html_content,image,keyword)",
                                                         values="('" + newsId + "','" + value[2] + "','" + value[4] + "','" +
                                                                value[1]
                                                                + "','" + value[6] + "','" + tag + "','" + value[
                                                                    10] + "','" + value[11] + "','" + value[12] + "','" + value[
                                                                   9] + "')")

                        if mysqlSuccess:
                            print("新闻保存sql完成!")
                    except:
                        # 出现错误则回滚
                        continue
        except:
            print("import failed")


newsInsert = newsInsert()