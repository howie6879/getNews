# -*-coding:utf-8-*-
__author__ = 'howie'
import pandas as pd
import os
import controller.newsController as newsController


class DataController(newsController.NewsController):
    def __init__(self):
        self.initData = self.newsFiles("get","allSource")

    def repeatedData(self,*dirs):
        """
        func:        对爬取的数据进行去重操作
        :param *dirs:文件夹list,dirs[0]里面含有文件夹名称,默认为2个
        :return:     成功返回True,否则返回"No Data"
        """
        if self.initData:
            for eachFile in self.initData:
                newsData = pd.read_excel(eachFile,sheetname="allNews")
                newsData = newsData.drop_duplicates()  # 去重
                # 获取主路径
                path = os.path.join(os.path.abspath('.'), 'spider')
                # 获取处理后文件路径
                for dir in dirs[0]:
                    path = os.path.join(path,dir)
                filePath = os.path.join(path, os.path.split(eachFile)[1])
                log = filePath + "文件去重成功"
                print(log)
                with open("./log.txt", 'a') as fp:
                    fp.write(log + "\n")
                newsData.to_excel(excel_writer=filePath, sheet_name="allNews")
            return True
        else:
            return "No Data!"

    def rmAllNews(self,newsSource):
        for i in newsSource:
            self.newsFiles("rm",i)
        return self.rmRepeate(['wordAna','allNews'])



newsSource = ["touTiaoSource","sinaSource","allSource"]
DataController = DataController()
#print(DataController.rmAllNews(newsSource))                     #删除所有原始数据
#print(DataController.initData)
#print(DataController.initData)
#DataController.rmRepeate(['wordAna','allNews'])            #删除去重文件夹里面的表
#DataController.rmRepeate(['wordAna','wordAnaNews'])            #删除分词文件夹里面的表
#print(DataController.repeatedData(['wordAna','allNews']))      #进行去重操作
