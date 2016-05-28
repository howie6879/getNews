# -*-coding:utf-8-*-
__author__ = 'howie'
import time
import os
import spider.toutiao.touTiaoSpider as ts
import spider.sina.sinaSpider as ss
import spider.mergeExcel as me
import spider.wordAna.contentSpider as cs

ss.cate = ["news_world", "news_sports", "news_finance", "news_society", "news_entertainment", "news_military",
           "news_tech"]


def getTimestamp(startTime):
    """
    Des:    将时间转化为时间戳
    param:  startTime="2016-05-17 12:00:00"(格式)
    return: timeStamp
    """
    timeArray = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def touTiao(category, page, num, time):
    # 爬取今日头条
    for cate in category:
        ts.getToutiaoNews(cate, page, num, time)


def sina(num=1000, page=1, type=ss.cate):
    # 爬取新浪新闻
    ss.getSinaNews(num, page, type)

def merge():
    #新闻合并操作
    mainPath = os.path.join(os.path.abspath('.'),'spider')
    secondPath = os.path.join(mainPath,'allSource')
    mergeExel = me.mergeExcel()
    mergeExel.merge(mainPath,secondPath)

def wordAna():
    cs.getNewsContent()

#touTiao(category=ts.category, page=2, num=20, time=time.time())
#sina()
#merge()
#wordAna()