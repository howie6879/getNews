# -*-coding:utf-8-*-
__author__ = 'howie'
import pandas as pd
import os
import newsController


class DataController(newsController.NewsController):
    def __init__(self):
        self.initData = self.touTiaoFiles("get")

    def repeatedData(self,*dirs):
        """
        func:       对爬取的数据进行去重操作
        :param *dirs:文件夹list,dirs[0]里面含有文件夹名称,默认为2个
        :return:    成功返回True
        """
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


DataController = DataController()
#DataController.rmRepeate(['toutiao','toutiaoNews'])        #删除去重文件夹里面的表
#print(DataController.touTiaoFiles("get"))                  #得到文件列表
#DataController.touTiaoFiles("rm")                          #删除原始新闻数据
