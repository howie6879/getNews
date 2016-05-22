#-*-coding:utf-8-*-
__author__ = 'howie'
import time
import toutiao.touTiaoSpider as ts

#爬取今日头条
for cate in ts.category:
    ts.getToutiaoNews(category=cate, page=1, time=time.time())
