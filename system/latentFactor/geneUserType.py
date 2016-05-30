# -*-coding:utf-8-*-
__author__ = 'Jeezy'

'''用户-标签（类型）潜在因子矩阵计算，与新闻-标签（类型）潜在因子矩阵相乘得到推荐新闻'''
'''数据表来源：用户行为信息表，存入标签喜欢程度表,计算方法是，通过用户行为信息表信息，计算各用户对各标签的喜欢程度'''


class getUserType:
    def __init__(self):
        # 总分数
        self.sumPoints = 0
        # 存每个用户对各个标签的偏爱值
        # 约定类型顺序，与NewsType对应，如0为全部，1为热点......
        self.typeCount = [0, 0, 0, 0, 0]
        self.judge = False

    def getData(self, typeWeight):
        # typeWeight对应的是每条全部新闻各自对应的类型和权重（分值）
        if self.judge == False:
            self.sumPoints = 0
            self.typeCount = [0, 0, 0, 0, 0]
            self.judge = True
        # 测试数据news（假设已获取正文）
        news = [["科技", 100], ["财经", 50], ["财经", 15], ["娱乐", 52], ["娱乐", 100], ["国内", 80], ["科技", 40], ["国际", 30]]
        self.proportionCul(news)
        return (self.typeCount)

    def proportionCul(self, typeWeight):
        for i in range(0, len(typeWeight)):
            self.sumPoints = self.sumPoints + typeWeight[i][1]
            if typeWeight[i][0] == "科技":
                self.typeCount[0] = typeWeight[i][1] + self.typeCount[0]
            if typeWeight[i][0] == "财经":
                self.typeCount[1] = typeWeight[i][1] + self.typeCount[1]
            if typeWeight[i][0] == "娱乐":
                self.typeCount[2] = typeWeight[i][1] + self.typeCount[2]
            if typeWeight[i][0] == "国内":
                self.typeCount[3] = typeWeight[i][1] + self.typeCount[3]
            if typeWeight[i][0] == "国际":
                self.typeCount[4] = typeWeight[i][1] + self.typeCount[4]
        # 计算用户对标签的偏爱程度（权重）
        self.typeWeight()

    def typeWeight(self):
        for i in range(0, len(self.typeCount)):
            self.typeCount[i] = self.typeCount[i] / self.sumPoints
        # print(self.typeCount)
        self.judge = False

# gut = getUserType()
# gut.getData(1)
