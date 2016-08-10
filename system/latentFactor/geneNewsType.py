# -*-coding:utf-8-*-

from methods.pDb import newsDb


class NewsTagDataTool(object):
    def __init__(self):
        #存新闻编号
        self.new_id_list = []
        self.newsTagMat = []

        #存取新闻id对应的类别
        self.news_type_dict = {}

    def getData(self):
        try:

            db = newsDb()
            data = db.select_table_two(table="news_tag_deep",column="*")

            for item in data:
                #获得新闻id
                self.new_id_list.append(item[0])
                #当前新闻标签比例因子集合，标签名称顺序按数据表设计来
                tagsWeight = []
                for tag in item[1:len(item)]:
                    tagsWeight.append(tag)
                self.newsTagMat.append(tagsWeight)

            datasql = "select news_id,tag from get_news where is_old = 0"
            data = db.select_table_three(datasql)
            # print(data)

            for item in data:
                #获取新闻的id及对应的类别：
                self.news_type_dict[item[0]] = item[1]

            #print(self.news_type_dict)
            # print(self.new_id_list)
            # print(self.newsTagMat)
            return self.news_type_dict,self.new_id_list,self.newsTagMat

        except Exception as e:
            print(e)

# ntTool = NewsTagDataTool()
# x,y,z=ntTool.getData()
# print(x)
# print(y)
#



