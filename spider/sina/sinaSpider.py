# -*-coding:utf-8-*-
__author__ = 'Jeezy'

from xlsxwriter import *
import os
import time
from sina.sina import GetSina


def getSinaNews(num, page, type):
    '''
	num每页新闻条数，page页数，一般设置page为1，控制变量
	'''
    allNewsData = []
    for page in range (0, page):
        sina = GetSina (num, page)
        allNewsData.append(sina.getNews ())
    choice (allNewsData, type)


def choice(data, type):
    # 分类字典,储存每一类的新闻
    allNews = {}
    allNews['news_world'] = []
    allNews['news_sports'] = []
    allNews['news_finance'] = []
    allNews['news_society'] = []
    allNews['news_entertainment'] = []
    allNews['news_military'] = []
    allNews['news_tech'] = []

    # 分类,将data的数据分类储存到字典里面
    for eachdata in data:
        for number in range (0, len (eachdata)):
            if eachdata [number] ['tag'] == "国内":
                eachdata [number]["tag"]="news_world"
                allNews ['news_world'].append (eachdata [number])
            if eachdata [number] ['tag'] == "体育":
                eachdata [number] ["tag"] = "news_sports"
                allNews ['news_sports'].append (eachdata [number])
            if eachdata [number] ['tag'] == "财经":
                eachdata [number] ["tag"] = "news_finance"
                allNews ['news_finance'].append (eachdata [number])
            if eachdata [number] ['tag'] == "社会":
                eachdata [number] ["tag"] = "news_society"
                allNews ['news_society'].append (eachdata [number])
            if eachdata [number] ['tag'] == "国际":
                eachdata [number] ["tag"] = "news_world"
                allNews ['news_world'].append (eachdata [number])
            if eachdata [number] ['tag'] == "娱乐":
                eachdata [number] ["tag"] = "news_entertainment"
                allNews ['news_entertainment'].append (eachdata [number])
            if eachdata [number] ['tag'] == "军事":
                eachdata [number] ["tag"] = "news_military"
                allNews ['news_military'].append (eachdata [number])
            if eachdata [number] ['tag'] == "美股":
                eachdata [number] ["tag"] = "news_finance"
                allNews ['news_finance'].append (eachdata [number])
            if eachdata [number] ['tag'] == "股市":
                eachdata [number] ["tag"] = "news_finance"
                allNews ['news_finance'].append (eachdata [number])
            if eachdata [number] ['tag'] == "科技":
                eachdata [number] ["tag"] = "news_tech"
                allNews ['news_tech'].append (eachdata [number])
    for ty in type:
        mkExel (ty, allNews[ty])
        # print (cate[dictNumber[i]])


def mkExel(cate, data):
    """
		将新闻数据生成excel表
		:param cate: 新闻类型
		:param data: 爬取的新闻数据
		:return:     返回生成的excel表
	"""
    # 设置excel表名称
    excelName = os.path.abspath ('.') + "/sinaSource/" + cate + "/" + str (
        time.strftime ('%Y-%m-%d-%H-%M-%S', time.localtime ())) + "&" + cate + "&" + str (len (data)) + ".xlsx"
    # 设置excel表名称
    jr_work = Workbook (excelName)
    jr_sheet = jr_work.add_worksheet ("sina")
    bold = jr_work.add_format ({'bold': True})  # 设置一个加粗的格式对象
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
        jr_sheet.write (line, 0, eachData ["title"])
        jr_sheet.write (line, 1, eachData ["display_url"])
        jr_sheet.write (line, 2, eachData ["display_time"])
        jr_sheet.write (line, 3, eachData ["source"])
        jr_sheet.write (line, 4, '')
        jr_sheet.write (line, 5, '')
        jr_sheet.write (line, 6, '')
        jr_sheet.write (line, 7, eachData ["tag"])
    jr_work.close ()
    log = "%s新闻表抓取完成,抓取数据%d条" % (excelName, line)
    with open ("log.txt", 'a') as fp:
        fp.write (log + "\n")
    print (log)

# getSinaNews(2000,1)
# 新闻种类
cate = ["news_world", "news_sports", "news_finance", "news_society", "news_entertainment", "news_military","news_tech"]