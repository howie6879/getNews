# -*-coding:utf-8-*-
__author__ = "xiao"

import math
import methods.db as db


class ScoreTool(object):
    def __init__(self):

        self.def_scan_time = 150.0
        self.conn = None
        self.cur = None

        #获取数据库连接及游标
        try:
            self.conn = db.conn
            # 获取游标
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)



    def scoreUpdate(self,user_id,new_id,tag,refer_time,operation):
        try:
            # 获取用户行为信息表中关于当前用户对当前类别新闻的行为数据
            all_new_info_list = self.getUserNewData(user_id,tag)
            #获取用户关于当前新闻的行为数据
            cur_new_info_list = self.getCurNewData(new_id,all_new_info_list)

            #获取当前新闻的类别比例因子字典
            cur_new_tagDeep_list = self.getCurNewTagList(new_id)

            #获取用户对当前类别新闻的平均浏览时间
            avgTime = self.calAvgTime(all_new_info_list)

            #在此行为之前用户对这条新闻的操作行为为空,或者最近一次行为的加分为0,无需考虑其他因素，主类加分可直接以当前行为进行计分
            if len(cur_new_info_list)==0 or cur_new_info_list[len(cur_new_info_list)-1][3]==None or cur_new_info_list[len(cur_new_info_list)-1][3]==0:
                score = self.calFirstAddScore(refer_time,operation,avgTime)

            #当用户连续两次操作为非删除操作时
            #此前已经有对于当前新闻的行为数据，代表此次行为对于用户类别之间的概括已经不能和第一次行为相比，更多的概括是在用户和此新闻涉及的话题之间
            #运用开平方的形式，保证每次加分都考虑到之前的行为，且保证加分幅度越来越小
            else:
                score = self.calNotFirstAddScore(operation,cur_new_info_list)

            #print(score)
            #由主类应加分数获得其他各类应加分数
            tagAddScoreDict = self.calAllTagAddScore(tag, score, cur_new_tagDeep_list)
            #print(tagAddScoreDict)
        except Exception as e:
            print("scoreUpdate raises the error")
            print(e)
        return score,tagAddScoreDict

    #计算 当前行为 对应的主类应加分数
    #此处为对当前新闻的第一次操作，不考虑是否有评论
    def calFirstAddScore(self,refer_time_str,operation,avgTime):
        #tag  当前用户浏览类别
        #refer_time   用户浏览该条新闻的时间(秒）
        #operation   用户对该条新闻的操作
        #is_comment  是否评论
        #用户浏览此类新闻的平均浏览时间

        #用户操作为浏览
        if operation==0:
            refer_time = (float)(refer_time_str)
            if refer_time <= avgTime:
                return 5.0
            elif refer_time >avgTime and refer_time <= 3*avgTime:
                return 5.0 + (refer_time - avgTime)/30.0     #此范围内，每过30秒加一分
            else:
                return 3/4.0 * ( 5.0 + 2*avgTime/30)

        #用户操作为喜欢
        elif operation == 1:
            return 3/4.0 * ( 5.0 + 2*avgTime/30)
        #用户操作为删除
        elif operation==2:
            return -3/4.0 * ( 5.0 + 2*avgTime/30)

    def calNotFirstAddScore(self,operation,cur_new_info_list):
        # 距离此次行为最近的一次行为加的分数
        org_score = cur_new_info_list[len(cur_new_info_list) - 1][3]

        if operation==2:
            #上一次操作也是删除
            if org_score<0:
                #降低删除带来的影响分，开平方
                score = - math.sqrt(-org_score)
            #上一次的操作不是删除，#减去上一次行为带来的加成分
            else:
                score = -org_score
        else:
            # 主类此次行为应加的分数
            score = math.sqrt(org_score)
        return score

    #根据当前新闻的比例因子计算各类别应加分数
    def calAllTagAddScore(self,tag,mainTagAddScore,cur_new_tagDeep_list):
        tagAddScore = {}
        mainTagDeep = 0.0
        for i in range(len(cur_new_tagDeep_list)):
            if i%2==0:
                if cur_new_tagDeep_list[i] == tag:
                    mainTagDeep = cur_new_tagDeep_list[i+1]
                    tagAddScore[tag] = mainTagAddScore

        for i in range(len(cur_new_tagDeep_list)):
            if i%2==0:
                if cur_new_tagDeep_list[i]!=tag:
                    tagAddScore[cur_new_tagDeep_list[i]] = mainTagAddScore * (cur_new_tagDeep_list[i+1]*1.0/mainTagDeep)

        return tagAddScore

    #计算用户浏览当前类别新闻的平均时间
    def calAvgTime(self,data):
            time_sum = 0.0          #浏览总时长
            news_sum = 0.0          #浏览新闻数
            if data!=None:
                for d in data:
                    #浏览时间存在时才能证明当前新闻被浏览过
                    if d[0]!=None:
                        if d[3]!=None:
                            time_sum += float(d[3])
                        news_sum += 1

            if news_sum==0.0:
                return self.def_scan_time

            avgTime = time_sum/news_sum
            #如果计算出来的平均浏览时间小于30秒，则代表数据不正常，强制定性用户浏览一条当前新闻的时间为默认花费时长
            if avgTime < 30:
                return self.def_scan_time

            return avgTime

    #获取用户行为信息表中关于当前用户对当前类别新闻的行为数据，包括新闻id,浏览新闻的时间，是否对新闻进行评论
    def getUserNewData(self,user_id,tag):
        if self.conn != None and self.cur != None:
            self.cur.execute(
                "select news_id,weight,is_comment,score from user_behavior where news_tag='" + tag + "' and user_id='" + user_id + "'")
            data = self.cur.fetchall()
            return data

        return None

    #获取用户对于当前此条新闻的行为数据
    def getCurNewData(self,new_id,news_info_list):
        cur_new_info_list = []
        if news_info_list!=None:
            for info in news_info_list:
                if info[0]==new_id:
                    cur_new_info_list.append(info)
        return cur_new_info_list

    #获取当前新闻的类别比重因子
    def getCurNewTagList(self,new_id):
        list = []
        if self.conn != None and self.cur != None:
            sql = "select * from news_tag_deep where news_id='" + new_id + "'"
            self.cur.execute(sql)
            data = self.cur.fetchone()
            if data!=None:
                for i in range(len(data)-1):
                  list.append(category[i])
                  list.append(float(data[i+1]))

            return list
        return None

# 新闻种类
category = ["news_society", "news_entertainment",
            "news_tech", "news_car", "news_sports", "news_finance", "news_military", "news_world",
            "news_fashion", "news_travel", "news_discovery", "news_baby", "news_regimen", "news_story",
            "news_essay", "news_game", "news_history", "news_food"]

st = ScoreTool()
# list = st.getCurNewTagList("050a797bb92b620722b6")
# st.calAllTagAddScore("news_society",5,list)
# x,y = st.scoreUpdate('000001','050a797bb92b620722b6',"news_travel",0,1)
# print(y)
