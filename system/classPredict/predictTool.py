#coding:utf-8

import math
import methods.db as db

class NavieBayesPredict(object):
    """使用训练好的模型进行预测"""
    def __init__(self,test_data_file,model_data_file,result_file):
        self.test_data_file = open(test_data_file,'r')
        self.model_data_file = open(model_data_file,'r')
        #对预测数据集预测的结果文件
        self.result_file = open(result_file,'w')

        #每个类别的先验概率
        self.class_probabilities = {}
        #拉普拉斯平滑，防止概率为0的情况出现
        self.laplace_smooth = 0.1
        #模型训练结果集
        self.class_word_prob_matrix = {}
        #当某个单词在某类别下不存在时，默认的概率（拉普拉斯平滑后）
        self.class_default_prob = {}
        #所有单词
        self.unique_words = {}
        #实际的新闻分类
        self.real_classes = []
        #预测的新闻分类
        self.predict_classes = []


    def __del__(self):
        self.test_data_file.close()
        self.model_data_file.close()

    def loadModel(self):
        #从模型文件的第一行读取类别的先验概率
        class_probs = self.model_data_file.readline().split('#')
        for cls in class_probs:
            arr = cls.split() 
            if len(arr)==3:
                self.class_probabilities[arr[0]] = float(arr[1])
                self.class_default_prob[arr[0]] = float(arr[2])

        #从模型文件读取单词在每个类别的概率
        line = self.model_data_file.readline().strip()
        while len(line)>0:
            arr = line.split()
            assert(len(arr)%2==1)
            assert(arr[0] in self.class_probabilities)
            self.class_word_prob_matrix[arr[0]] = {}
            i = 1
            while i<len(arr):
                word_id = int(arr[i])
                probability = float(arr[i+1])
                if word_id not in self.unique_words:
                    self.unique_words[word_id] = 1
                self.class_word_prob_matrix[arr[0]][word_id] = probability
                i = i+2

            line = self.model_data_file.readline().strip()

        print(len(self.class_probabilities),"classes loaded!",len(self.unique_words),"words!")

    def caculate(self):

        # 读取测试数据集
        line = self.test_data_file.readline().strip()

        while len(line)>0:
            arr = line.split()
            new_id = arr[0]

            # class_id = arr[1]
            # print(class_id)

            words = arr[1:len(arr)-1]

            #把真实的分类保存起来
            # self.real_classes.append(class_id)

            #预测当前行（一个新闻）属于各个分类的概率
            class_score = {}
            for key in self.class_probabilities.keys():
                class_score[key] = math.log(self.class_probabilities[key])
            for word_id in words:
                word_id = int(word_id)

                for class_id in self.class_probabilities.keys():
                    if word_id not in self.class_word_prob_matrix[class_id]:
                        class_score[class_id] += math.log(self.class_default_prob[class_id])
                    else:
                        class_score[class_id] += math.log(self.class_word_prob_matrix[class_id][word_id])



            #对于当前新闻类别值，进行正数转换，加上最低限度
            needAdd = -(min(class_score.values())) + 1

            #开始将所有分数转化为正数,并计算分数总和
            sum = 0.0
            for key in class_score.keys():
                class_score[key] += needAdd
                sum = sum + class_score[key]

            #开始计算比例因子
            for key in class_score.keys():
                class_score[key] = class_score[key]/sum
                # print(key + ":" + str(class_score[key]))

            # 将当前新闻的比例因子数据存进数据库
            self.saveToDb(new_id, class_score)

            line = self.test_data_file.readline().strip()

        #提交总体sql事务
        db.conn.commit()

    # def evaluation(self):
    #     #评价当前分类器的准确性
    #     accuracy = 0
    #     i = 0
    #     while i<len(self.real_classes):
    #         if self.real_classes[i] == self.predict_classes[i]:
    #             accuracy += 1
    #         i += 1
    #
    #     accuracy = (float)(accuracy)/(float)(len(self.real_classes))
    #     print("Accuracy:",accuracy)
    #
    #     # 评测精度和召回率
    #     # 精度是指所有预测中，正确的预测
    #     # 召回率是指所有对象中被正确预测的比率
    #     for class_id in self.class_probabilities:
    #         correctNum = 0
    #         allNum = 0
    #         predNum = 0
    #         i = 0
    #
    #         while i<len(self.real_classes):
    #             if self.real_classes[i] == class_id:
    #                 allNum += 1
    #                 if self.predict_classes[i] == self.real_classes[i]:
    #                     correctNum += 1
    #             if self.predict_classes[i] == class_id:
    #                 predNum += 1
    #             i += 1
    #         precision = (float)(correctNum)/(float)(predNum)
    #         recall = (float)(correctNum)/(float)(allNum)
    #         print (class_id,'->precision=',precision,'recall=',recall)

    def saveToDb(self,new_id,class_score):
        list = [str(class_score["society"]),str(class_score["entertainment"]),str(class_score["tech"]),str(class_score["car"]),
                          str(class_score["sports"]),str(class_score["finance"]),str(class_score["military"]),str(class_score["world"]),
                          str(class_score["fashion"]),str(class_score["travel"]),str(class_score["discovery"]),str(class_score["baby"]),
                          str(class_score["regimen"]),str(class_score["story"]),str(class_score["essay"]),str(class_score["game"]),
                          str(class_score["history"]),str(class_score["food"])]

        tmpstr = ','.join(list)
        sql = "insert into news_tag_deep values('" + new_id+ "'," + tmpstr + ")"

        db.cur.execute(sql)
        print("存储" + new_id + "新闻的类别偏重比例")

    def predict(self):
        self.loadModel()
        self.caculate()
        # self.evaluation()









