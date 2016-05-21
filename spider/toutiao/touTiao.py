#-*-coding:utf-8-*-
__author__ = 'howie'

import requests
import time
import json

class GetToutiao():
    """
    通过今日头条API获取新闻信息,保存至本地excel
    """
    def __init__(self,count,category,time=time.time()):
        self.count = count
        self.category = category
        self.time = time
        self.url = "http://toutiao.com/api/article/recent/?count="+count+"&category="+(category)+"&max_behot_time="+str(time)

    def getNews(self):
        try:
            news = requests.get(self.url)
            newsJson = json.loads(news.text)
            allNewsData = []
            if newsJson["data"]:
                for eachData in newsJson["data"]:
                    newsData = {}
                    newsData["title"] = eachData["title"]
                    newsData["display_url"] = eachData["display_url"]
                    newsData["display_time"] = eachData["display_time"]
                    newsData["source"] = eachData["source"]
                    newsData["keywords"] = eachData["keywords"]
                    newsData["abstract"] = eachData["abstract"]
                    if "middle_image" in eachData.keys():
                        newsData["images"] = eachData["middle_image"]
                    else:
                        newsData["images"] = "null"
                    newsData["tag"] = eachData["tag"]
                    allNewsData.append(newsData)
            else:
                exit("no data!")
            return allNewsData
        except ConnectionError:
            exit("ConnectionError")