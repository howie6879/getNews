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
        data = pd.read_excel(file,sheetname="allNews")
        data = data.drop_duplicates(subset='title', keep='last')
        db = newsDb ()
        for i in range(0, len(data) ):
            value = data.values[i]
            if value[10] and value[11]:
                times = time.time()
                md5newid = hashlib.md5(str(times).encode("utf-8")).hexdigest()
                startNum = random.randint(0, (len(md5newid) - 20))
                newsId = str(md5newid)[startNum:(startNum + 20)]
                try:

                    mysqlSuccess = db.insert_table(table="get_news", field="(news_id,news_link,source,title,abstract,tag,"
                                                                             "text_content,html_content,image,keyword)",
                                                     values="('" + newsId + "','" + value[2] + "','" + value[4] + "','" +
                                                            value[1]
                                                            + "','" + value[6] + "','" + value[8] + "','" + value[
                                                                10] + "','" + value[11] + "','" + value[12] + "','" + value[
                                                               9] + "')")

                    if mysqlSuccess:
                        print("新闻保存sql完成!")
                except:
                    # 出现错误则回滚
                    print("404")


newsInsert = newsInsert()