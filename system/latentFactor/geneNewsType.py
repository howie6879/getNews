# -*-coding:utf-8-*-
__author__ = 'Jeezy'

'''新闻-标签（类型）潜在因子矩阵计算，与用户-标签（类型）潜在因子矩阵相乘得到推荐新闻'''
'''数据表来源：新闻数据表，存入：新闻标签因子表,然后分析各个新闻各个标签对应的偏值（权重）。分析的方法是计算主要特征词（由计算得到）在各新闻中所占比值'''

#import geneUserNews as gut
class getNewsType:
    def __init__(self):
        #存新闻编号
        self.newsNum = []
        #总分数
        self.sumPoints = 0
        #存新闻编号对应的类型所占比重
        self.typeCount = []
        self.judge = False




    def getData(self,content):
        #用户编号（暂不用），新闻编号，用户-新闻潜在因子矩阵
        #这里肯定要根据编号获取新闻 正文，如不能，就传链接参数
        #userdata, ndata, geneData = gut.userGet()
        # 测试数据（假设已获取正文）
        if self.judge == False:
            # 存新闻编号
            self.newsNum = []
            # 总分数
            self.sumPoints = 0
            # 存新闻编号对应的类型所占比重
            self.typeCount = []
            self.judge = True
        news = ["你好，热北京包括价格额不分分工你好认同别人和人工好，你安徽你好恶和感染"]

        #return news
        self.proportionCul(news[0])
        return(self.typeCount)
        #print(self.typeCount)
        #print(self.userNum)


    def proportionCul(self,content):
        #计算新闻编号对应的类型所占比重,并将新闻编号及比重放进其对应矩阵
        #约定好顺序，与UserType对应,如：0为全部，1为热点......
        #print(num,content)
        #exit()
        #科技
        a =content.count("你好") +content.count("你好")+content.count("你好")+content.count("你好")+content.count("你好")
        self.typeCount.insert(0,a)
        # 科技
        b = content.count ("工") + content.count ("和") + content.count ("工") + content.count ("工") + content.count ("好")
        self.typeCount.insert (0, b)
        # 科技
        c = content.count ("你") + content.count ("你好") + content.count ("工") + content.count ("工") + content.count ("你好")
        self.typeCount.insert (0, c)
        # 科技
        d = content.count ("好") + content.count ("你好") + content.count ("工") + content.count ("你好") + content.count ("和")
        self.typeCount.insert (0, d)
        # 科技
        e = content.count ("好") + content.count ("工") + content.count ("好") + content.count ("和") + content.count ("你好")
        self.typeCount.insert (0, e)
        #......
        # 计算各类型总分数
        self.sumPoints = self.sumPoints + a + b + c + d + e  # 各类型分数相加
        # 计算偏值（权重）
        self.typeWeight ()

    def typeWeight(self):
        # 计算偏值（权重）
        for i in range(0,len(self.typeCount)):
            self.typeCount[i] = self.typeCount[i]/self.sumPoints
        self.judge = False
        #print(self.typeCount)
        #return(self.typeCount)

#gnt = geneNewsType()
#gnt.getData(1)
