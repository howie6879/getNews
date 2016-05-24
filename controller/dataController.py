# -*-coding:utf-8-*-
__author__ = 'howie'
import pandas as pd
import os
import newsController


class DataController(newsController.NewsController):
    def __init__(self,sourceName):
        self.initData = self.newsFiles("get",sourceName)

    def repeatedData(self,*dirs):
        """
        func:        对爬取的数据进行去重操作
        :param *dirs:文件夹list,dirs[0]里面含有文件夹名称,默认为2个
        :return:     成功返回True,否则返回"No Data"
        """
        if self.initData:
            for eachFile in self.initData:
                newsData = pd.read_excel(eachFile)
                newsData = newsData.drop_duplicates()  # 去重
                # 获取主路径
                path = os.path.join(os.path.dirname(os.path.abspath('.')), 'spider')
                # 获取处理后文件路径
                for dir in dirs[0]:
                    path = os.path.join(path,dir)
                filePath = os.path.join(path, os.path.split(eachFile)[1])
                log = filePath + "文件去重成功"
                print(log)
                with open("../spider/log.txt", 'a') as fp:
                    fp.write(log + "\n")
                newsData.to_excel(excel_writer=filePath, sheet_name=dirs[0][0])
            return True
        else:
            return "No Data!"

newSource = ["touTiaoSource","sinaSource"]
DataController = DataController(newSource[1])
#print(DataController.initData)
#print(DataController.initData)
DataController.rmRepeate(['allSource','allNews'])        #删除去重文件夹里面的表
#DataController.newsFiles("rm",newSource[1])                          #删除原始新闻数据
#print(DataController.repeatedData(['allSource','allNews']))
