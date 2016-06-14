# -*-coding:utf-8-*-
__author__ = 'Jeezy'

'''通过geneNewsType和geneUserType计算出最终的用户-新闻矩阵，即推荐新闻表'''

# from geneNewsType import NewsTagDataTool
# from geneUserType import UserTagDataTool
from system.latentFactor.geneNewsType import NewsTagDataTool
from system.latentFactor.geneUserType import UserTagDataTool
import methods.db as db
import traceback


class GeneCulcal:
    def __init__(self):
        # 新闻-标签  矩阵
        self.newsType = []
        # 用户-标签  矩阵
        self.userType = []
        # 用户-新闻  矩阵
        self.userNews = []

        #新闻id集合
        self.new_id_list = []

        #用户id集合
        self.user_id_list = []

        #新闻id和类别的映射字典
        self.news_type_dict = None

        #获取各矩阵的各操作类
        self.ntTool = NewsTagDataTool()

        self.utTool = UserTagDataTool()

    # 每一个矩阵,及对应id集合的获取和计算
    def getMatData(self):
        try:

            self.news_type_dict,self.new_id_list,self.newsType = self.ntTool.getData()
            self.user_id_list,self.userType = self.utTool.getData()
            self.finalCalcul()
            self.saveToDb()
        except Exception as e:
            exstr = traceback.format_exc()
            print(exstr)




    def finalCalcul(self):
        try:
            for i in range(0, len(self.userType)):
                append = []
                for j in range(0, len(self.newsType)):
                    sum = 0
                    for n in range(0, len(self.newsType[j])):
                        sum = sum + self.newsType[j][n] * self.userType[i][n]
                    append.insert(j, sum)
                self.userNews.append(append)
        except Exception as e:
            exstr = traceback.format_exc()
            print(exstr)


        # print(self.userNews)



    def saveToDb(self):

        conn = db.conn
        # 获取游标
        cur = conn.cursor()


        user_id_score_dict = {}
        #use the user_id_list to initalize the user_id_score_dict
        for user_id in self.user_id_list:
            user_id_score_dict[user_id] = None

        cur.execute("select * from news_recommend")
        data = cur.fetchall()
        for d in data:
            if d[1] == None:
                user_id_score_dict[d[0]] = None
            #美元符号代表两次计算结果的拼接,如果发现美元符号，则取最后一次拼接，即最后一次计算结果
            elif d[1].find('$')!=-1:
                arr = d[1].split('$')
                user_id_score_dict[d[0]] = arr[len(arr)-1]
            else:
                user_id_score_dict[d[0]] = d[1]

        #行：用户id    列：新闻id
        for i in range(len(self.user_id_list)):
            list = []
            tmp_news_tag_deep = {}

            for j in range(len(self.new_id_list)):
                tmp_news_tag_deep[self.new_id_list[j]] = self.userNews[i][j]

            sorted_news_tag_deep = sorted(tmp_news_tag_deep.items(),key=lambda d:d[1],reverse=True)

            for d in sorted_news_tag_deep:
                if self.news_type_dict.get(d[0],None)!=None:
                    list.append(d[0]+ "+" + self.news_type_dict[d[0]] + "+" +  str(d[1]))


            tmpstr = '#'.join(list)
            print(tmpstr)
            #if the table named news_recommend has not the id of this user,we should insert the data.
            if user_id_score_dict[self.user_id_list[i]] == None:
                cur.execute("insert into news_recommend value('" + self.user_id_list[i] + "','" + tmpstr + "')")
            else:
                updateStr = user_id_score_dict[self.user_id_list[i]] + "$" + tmpstr
                # 更新数据表news_recommend
                cur.execute ("update news_recommend set news_score = '" + updateStr + "' where user_id='" + self.user_id_list [i] + "'")
            print(str(i))
        conn.commit()



# gc = GeneCulcal()
# 14715714711