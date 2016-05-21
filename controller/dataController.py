# -*-coding:utf-8-*-
__author__ = 'howie'
import pandas as pd
import os
import newsController


class DataController(newsController.NewsController):
    def __init__(self):
        self.initData = self.touTiaoFiles("get")

    def repeatedData(self):
        """
        func:       对爬取的数据进行去重操作
        :return:    成功返回True
        """
        for eachFile in self.initData:
            newsData = pd.read_excel(eachFile)
            newsData = newsData.drop_duplicates()  # 去重
            # 获取主路径
            path = os.path.dirname(os.path.abspath('.'))
            # 获取处理后文件路径
            path = os.path.join(os.path.join(path, 'spider'), 'toutiao')
            path = os.path.join(os.path.join(path, 'toutiaoNews'),os.path.split(eachFile)[1])
            log = path+"文件去重成功"
            print(log)
            with open("../spider/log.txt", 'a') as fp:
                fp.write(log + "\n")
            newsData.to_excel(excel_writer=path, sheet_name="toutiao")
        return True

# DataController = DataController()
# DataController.repeatedData()
