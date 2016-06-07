# -*-coding:utf-8-*-
__author__ = 'howie'
from xlsxwriter import *
import time
import datetime
import os
from random import choice
from spider.toutiao.touTiao import GetToutiao


def getToutiaoNews(category, page, num):
    """
    Des:    返回今日头条新闻
    param:
    category:新闻类型,默认为__all__
    page    :爬取页面,默认20页
    num     :每页新闻数量,根据今日头条每页返回数量变化,默认参数为20
    ctime    :新闻时间,根据标准库time.time()获取
    return: /source/下各文件夹
    """
    newsData = []
    for page in range(0, page):
        # ltime = [time.time(),"1464710423","1464796865","1464753667","1464840044","1464883266"]
        # ctime = choice(ltime)
        # print(ctime)
        # 获取两天前的时间
        twoDayAgo = (datetime.datetime.now() - datetime.timedelta(days=1))
        # 转换为时间戳:
        timeStamp = int(time.mktime(twoDayAgo.timetuple()))
        ctime = choice(range(timeStamp, int(time.time())))
        toutiao = GetToutiao(str(num), category, ctime)
        allNewsData = toutiao.getNews()
        for news in allNewsData:
            newsData.append(news)
    mkExcel(category, newsData)


def getTimestamp(startTime):
    """
    Des:    将时间转化为时间戳
    param:  startTime="2016-05-17 12:00:00"(格式)
    return: timeStamp
    """
    timeArray = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def mkExcel(cate, data):
    """
    将新闻数据生成excel表
    :param cate: 新闻类型
    :param data: 爬取的新闻数据
    :return:     返回生成的excel表
    """
    # 设置excel表名称
    excelName = os.path.abspath('.') + "/spider/touTiaoSource/" + cate + "/" + str(
        time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())) + "&" + cate + "&" + str(len(data)) + ".xlsx"
    # 设置excel表名称
    jr_work = Workbook(excelName)
    jr_sheet = jr_work.add_worksheet("toutiao")
    bold = jr_work.add_format({'bold': True})  # 设置一个加粗的格式对象
    jr_sheet.set_column('A:H', 40)
    jr_sheet.set_column('C:D', 15)
    jr_sheet.write(0, 0, '标题', bold)
    jr_sheet.write(0, 1, '发表地址', bold)
    jr_sheet.write(0, 2, '发表时间', bold)
    jr_sheet.write(0, 3, '来源', bold)
    jr_sheet.write(0, 4, '关键词', bold)
    jr_sheet.write(0, 5, '摘要', bold)
    jr_sheet.write(0, 6, '图片地址', bold)
    jr_sheet.write(0, 7, '标签', bold)
    line = 0
    for eachData in data:
        line += 1
        jr_sheet.write(line, 0, eachData["title"])
        jr_sheet.write(line, 1, eachData["display_url"])
        jr_sheet.write(line, 2, eachData["display_time"])
        jr_sheet.write(line, 3, eachData["source"])
        jr_sheet.write(line, 4, eachData["keywords"])
        jr_sheet.write(line, 5, eachData["abstract"])
        jr_sheet.write(line, 6, str(eachData["images"]))
        jr_sheet.write(line, 7, eachData["tag"])
    jr_work.close()
    log = "%s新闻表抓取完成,抓取数据%d条" % (excelName, line)

    with open("log.txt", 'a') as fp:
        fp.write(log + "\n")
    print(log)


# 新闻种类
category = ["news_society", "news_entertainment",
            "news_tech", "news_car", "news_sports", "news_finance", "news_military", "news_world",
            "news_fashion", "news_travel", "news_discovery", "news_baby", "news_regimen", "news_story",
            "news_essay", "news_game", "news_history", "news_food"]
