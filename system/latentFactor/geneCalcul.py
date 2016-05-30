# -*-coding:utf-8-*-
__author__ = 'Jeezy'

'''通过geneNewsType和geneUserType计算出最终的用户-新闻矩阵，即推荐新闻表'''

from geneNewsType import getNewsType
from geneUserType import getUserType


class geneCulcal:
    def __init__(self):
        # 新闻-标签  矩阵
        self.newsType = []
        # 用户-标签  矩阵
        self.userType = []
        # 用户-新闻  矩阵
        self.userNews = []

    def getData(self):
        # 每一个矩阵的获取和计算
        self.getDbNewsType()
        self.getDbUserType()
        self.finalCalcul()

    def getDbNewsType(self):
        # 原始数据从数据库获取
        # 测试数据
        newsContent = [[1, "这是第1条新闻的正文测试数据"], [2, "这是第2条新闻的正文测试数据"], [3, "这是第3条新闻的正文测试数据"], [4, "这是第4条新闻的正文测试数据"]]
        self.calculNewsType(newsContent)

    def calculNewsType(self, newsContent):
        gnt = getNewsType()
        for item in newsContent:
            # self.ntGetData(item)
            get = gnt.getData(item)
            self.newsType.append(get)

    def getDbUserType(self):
        # 查询每个用户看过的新闻的编号，并通过编号获取每条新闻的类型和历史评分
        # 测试数据
        # 这里根据用户的数量循环，每一次传入一个用户的所有新闻对应的类型和权重
        for i in range(0, 6):
            typeWeight = [["科技", 100], ["财经", 50], ["财经", 15], ["娱乐", 52], ["娱乐", 100], ["国内", 80], ["科技", 40],
                          ["国际", 30]]
            self.calculUserType(typeWeight)

    def calculUserType(self, typeWeight):
        gut = getUserType()
        get = gut.getData(typeWeight)
        self.userType.append(get)

    def finalCalcul(self):
        for i in range(0, len(self.userType)):
            append = []
            for j in range(0, len(self.newsType)):
                sum = 0
                for n in range(0, len(self.newsType[j])):
                    sum = sum + self.newsType[j][n] * self.userType[i][n]
                append.insert(j, sum)
            self.userNews.append(append)
        #print(self.newsType)
        for i in self.newsType:
            print(i)
        #print(self.userType)
        print("\n")
        for j in self.userType:
            print(j)
        print("\n")
        #print(self.userNews)
        for k in self.userNews:
            print(k)


gc = geneCulcal()
gc.getData()
