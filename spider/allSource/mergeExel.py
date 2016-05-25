# -*-coding:utf-8-*-
__author__ = 'Jeezy'

from xlsxwriter import *
import os
import xlrd
import time


class mergeExel:
    def __init__(self):
        self.mergeSuccess = False
        #定义一个字典分类储存合并后的新闻
        self.allNews = {}
        self.allNews ['__all__'] = []
        self.allNews ['news_hot'] = []
        self.allNews ['video'] = []
        self.allNews ['gallery_detail'] = []
        self.allNews ['news_society'] = []
        self.allNews ['news_entertainment'] = []
        self.allNews ['news_tech'] = []
        self.allNews ['news_car'] = []
        self.allNews ['news_sports'] = []
        self.allNews ['news_finance'] = []
        self.allNews ['news_military'] = []
        self.allNews ['news_world'] = []
        self.allNews ['news_fashion'] = []
        self.allNews ['news_travel'] = []
        self.allNews ['news_discovery'] = []
        self.allNews ['news_baby'] = []
        self.allNews ['news_regimen'] = []
        self.allNews ['news_story'] = []
        self.allNews ['news_essay'] = []
        self.allNews ['news_game'] = []
        self.allNews ['news_history'] = []
        self.allNews ['news_food'] = []
        # 定义新闻类型列表
        self.category = ["__all__", "news_hot", "video", "gallery_detail", "news_society", "news_entertainment",
                    "news_tech", "news_car", "news_sports", "news_finance", "news_military", "news_world",
                    "news_fashion", "news_travel", "news_discovery", "news_baby", "news_regimen", "news_story",
                    "news_essay", "news_game", "news_history", "news_food", ]
        # 定义网站列表,如有新增网站，可在此添加用于合并
        self.newsSourse = ["sinaSource", "touTiaoSource"]
    def merge(self):
        # 获取主路径
        mainPath = os.path.dirname (os.path.abspath ('.'))
        # 获取新闻目录
        #path = os.path.join (os.path.join (mainPath, 'spider'), newsSourse[0])
        for typeSourse in self.newsSourse:
            path = os.path.join (mainPath, typeSourse)
            for dir in os.listdir (path):
                dirPath = os.path.join (path, dir)
                if os.path.isdir (dirPath):
                    files = [file for file in os.listdir (dirPath) if
                             os.path.isfile (os.path.join (dirPath, file)) and os.path.splitext (file) [1] == ".xlsx"]
                    if files:
                        for file in files:
                            #conserve,提取exel表数据，并合并
                            # 传数据,新闻类型:file.split('&')[1],该类型对应的exel名:file，该类型对应的地址:os.path.join (dirPath,file)
                            self.conserve(file.split('&')[1],file,os.path.join (dirPath,file))

        #调用mkexel写将数据循环写入exel
        for cate in self.category:
            self.mkExel(cate,self.allNews [cate])

    # conserve,提取exel表数据，并合并
    def conserve(self,cate,excelData,dir):
        #新闻类型:cate,该类型对应的exel名:excelData，该类型对应的地址:dir
        data = xlrd.open_workbook (dir)
        table = data.sheets () [0]
        nrows = table.nrows
        for i in range (1, nrows):
            value = table.row_values (i)
            #judgeType:判断类型，找到对应的类型，分类储存到self.allNews
            self.judgeType(cate,value)
        #print(self.allNews [cate])

    def judgeType(self,cate,value):
        for ca in self.category:
            if cate ==ca:
                self.allNews [cate].append (value)
                #print(self.allNews [cate])

    def mkExel(self,cate, data):
        """
    		将新闻数据生成excel表
    		:param cate: 新闻类型
    		:param data: 爬取的新闻数据
    		:return:     返回生成的excel表
    	"""
        # 设置excel表名称
        excelName = os.path.abspath ('.') + "/" + cate + "/" + str (
            time.strftime ('%Y-%m-%d-%H-%M-%S', time.localtime ())) + "&" + cate + "&" + str (len (data)) + ".xlsx"
        # 设置excel表名称
        jr_work = Workbook (excelName)
        jr_sheet = jr_work.add_worksheet ("allNews")
        bold = jr_work.add_format ({'bold': True})  # 设置一个加粗的格式对象
        jr_sheet.set_column ('A:H', 40)
        jr_sheet.set_column ('C:D', 15)
        jr_sheet.write (0, 0, '标题', bold)
        jr_sheet.write (0, 1, '发表地址', bold)
        jr_sheet.write (0, 2, '发表时间', bold)
        jr_sheet.write (0, 3, '来源', bold)
        jr_sheet.write (0, 4, '关键词', bold)
        jr_sheet.write (0, 5, '摘要', bold)
        jr_sheet.write (0, 6, '图片地址', bold)
        jr_sheet.write (0, 7, '标签', bold)
        line = 0
        for eachData in data:
            line += 1
            jr_sheet.write (line, 0, eachData [0])
            jr_sheet.write (line, 1, eachData [1])
            jr_sheet.write (line, 2, eachData [2])
            jr_sheet.write (line, 3, eachData [3])
            jr_sheet.write (line, 4, eachData [4])
            jr_sheet.write (line, 5, eachData [5])
            jr_sheet.write (line, 6, str (eachData [6]))
            jr_sheet.write (line, 7, eachData [7])
        jr_work.close ()
        log = "%s新闻数据合并完成，共合并数据%d条" % (excelName, line)
        with open ("../log.txt", 'a') as fp:
            fp.write (log + "\n")
        print (log)
        self.mergeSuccess = True



mer = mergeExel()
mer.merge()