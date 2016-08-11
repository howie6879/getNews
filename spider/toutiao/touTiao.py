# -*-coding:utf-8-*-
__author__ = 'howie'

import sys, time, json, requests


class GetToutiao():
    """
    通过今日头条API获取新闻信息,保存至本地excel
    """

    def __init__(self, count, category, time):
        self.count = count
        self.category = category
        self.time = time
        self.url = "http://toutiao.com/api/article/recent/?count=" + count + "&category=" + category + "&as=A1D5A7DACCA0188&cp=57AC60B1C8C89E1&_=" + str(
            time)

    def getNews(self):
        print(self.url)
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
            root = requests.get("http://toutiao.com/", headers=header)
            news = requests.get(self.url, headers=header, cookies=root.cookies)
            allNewsData = []
            try:
                news = str(news.text).strip("'<>() ").replace('\'', '\"')
                newsJson = json.loads(news)
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
            except:
                print(repr(news))
                print(sys.exc_info())
            return allNewsData
        except ConnectionError:
            exit("ConnectionError")

# for i in range(1,20):
#     get = GetToutiao("30", "news_society", time.time())
#     allNewsData = get.getNews()
#     for i in allNewsData:
#         print(i)
