
import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
import codecs


class ContentOperator():
    """
    通过excel表中的链接获取对应网页新闻的正文
    """

    def __init__(self):
        pass


    """
    :param url为待爬取的网页链接
    """
    def getContent(self,url):
        try:
            print (url)
            newstr = requests.get(url).content.decode("utf-8")      #获取对应网页html正文
            # new =  etree.HTML(newstr)
            # header = new.xpath(u"//div[@id='pagelet-article']/div[@class='article-header']")[0]
            # content = new.xpath(u"//div[@id='pagelet-article']/div[@class='article-content']")[0]

            soup = BeautifulSoup(newstr,"lxml")
            header = soup.find('div',class_="article-header")
            content = soup.find('div',class_="article-content")
            htmlContent = str(header) + str(content)
            textContent = self.parseHtml(htmlContent)
            # print(textContent)
            return textContent,htmlContent

        except ConnectionError:
            exit("ConnecttionError")


    """
    :param htmlContent为要解析为纯文本的html正文
    """
    def parseHtml(self,htmlContent):
        pt = re.compile(r'<[^>]+>',re.S)
        return pt.sub('',htmlContent)

