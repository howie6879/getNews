# -*- coding: utf-8 -*
__author__ = 'Jeezy'

import os
import xlrd
import time
import hashlib
import methods.db as mSql
import random


class newsInsert:
    def __init__(self):
        pass

    def insertSql(self, mainPath):
        path = os.path.abspath('.') + "/spider/wordAna/" + mainPath
        for dir in os.listdir(path):
            # print(dir)
            if os.path.splitext(dir)[1] == ".xlsx":
                file = os.path.join(path, dir)
                self.insert(file)

    def insert(self, dir):
        data = xlrd.open_workbook(dir)
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(1, nrows):
            value = table.row_values(i)
            times = time.time()
            md5newid = hashlib.md5(str(times).encode("utf-8")).hexdigest()
            startNum = random.randint(0, (len(md5newid) - 20))
            newsId = str(md5newid)[startNum:(startNum + 20)]
            try:
                mysqlSuccess = mSql.insert_table(table="get_news", field="(news_id,news_link,source,title,abstract,tag,"
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
                mSql.conn.rollback()


newsInsert = newsInsert()
