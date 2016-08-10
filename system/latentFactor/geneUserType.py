# -*-coding:utf-8-*-

from methods.pDb import newsDb

'''用户-标签（类型）潜在因子矩阵计算，与新闻-标签（类型）潜在因子矩阵相乘得到推荐新闻'''
'''数据表来源：用户行为信息表，存入标签喜欢程度表,计算方法是，通过用户行为信息表信息，计算各用户对各标签的喜欢程度'''


class UserTagDataTool(object):
    def __init__(self):

        #存储各用户的id
        self.user_id_list = []
        #存储各用户对各类别的喜欢比例
        self.userTagMat = []

    def getData(self):
        try:
            db = newsDb()
            data = db.select_table_two(table="user_tag_score",column="*")
            for item in data:
                # 获得用户id
                self.user_id_list.append(item[0])
                # 当前用户对各类别的新闻的分数的集合，类别名称顺序按数据表设计来
                tagsScore = []
                curSum = 0
                for score in item[1:len(item)]:
                    if score == None:
                        tmp = 1
                    else:
                        tmp = float(score)

                    curSum = curSum + tmp
                    tagsScore.append(tmp)

                #当前用户对于各类别的喜欢比重，类别名称顺序按数据表设计来
                tagsWeight = []
                for i in range(0,len(tagsScore)):
                    tagsWeight.append(tagsScore[i]/(float)(curSum))

                self.userTagMat.append(tagsWeight)
            # print(self.user_id_list)
            # print(self.userTagMat)
            return self.user_id_list,self.userTagMat
        except Exception as e:
            print(e)


# gut = UserTagDataTool()
# x,y = gut.getData()
# print(x)
# print(y)