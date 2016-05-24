#-*-coding:utf-8-*-
__author__ = 'Jeezy'

import requests
import re

class GetSina():
	'''
	通过网易新闻API获取新闻信息，保存至exel
	'''
	def __init__(self,num,page):
		self.num = str(num)
		self.page = str(page)
		self.url = "http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&k=&num="+self.num+"&asc=&page="+self.page+"&r=0.41627189057293945"
	def getNews(self):
		#通过API爬取新浪新闻文本内容
		gettext = requests.get(self.url)
		gettext.encoding='gbk'
		gettext = gettext.text
		allNewsData = []
		patten = re.compile('channel : {title : "(.*?)",id.*?title : "(.*?)",url : "(.*?)",type.*?time : (.*?)}',re.S)
		items = re.findall(patten,gettext)
		for eachData in items:
			newsData = {}
			newsData["tag"] = eachData[0]
			newsData["title"] = eachData[1]
			newsData["display_url"] = eachData[2]
			newsData["display_time"] = eachData[3]
			newsData["source"] = "新浪新闻"
			allNewsData.append(newsData)
		return allNewsData
			#if allNewsData[0]['tag']== "体育":
			#print (allNewsData)

#sina =GetSina(5,1)
#sina.getNews()