import os
import re
import jieba
import jieba.analyse
from spider.wordAna.contentTool import ContentOperator
from spider.wordAna.excelTool import ExcelOperator
from config.n_conf import dirPath

class DataPerpare(object):
    def __init__(self,dataDir):
        #存放训练数据的文件夹，训练数据统一为excel文件
        self.dataDir = dataDir

        # 获得excelTools.py中的excel操作工具
        self.et = ExcelOperator()
        # 获得contentTools.py中的content操作工具
        self.ct = ContentOperator()

        # 使用该txt文件存储各类别新闻数等相关信息
        self.fn = open(dirPath + "/system/classPredict/NavieBayesInfo/train_news_Info.txt", "a")

        # 要将单词与id的字典放到txt文件中，以此进行贝叶斯分类时的使用准备
        self.fd = open(dirPath + "/system/classPredict/NavieBayesInfo/word_id_dict.txt", 'a')

        # 文件行数据格式 类别 单词1 单词2 单词3#类别
        # 对于每个单词，使用一个id表示，提高检索速度=====word_ids
        # 一个包含所有不重复单词的集合====unique_words
        self.unique_words = []
        self.word_ids = {}

    def getNewContentAndAnalyse(self):
        #获取所有存放训练数据的excel文件的集合
        filenames = self.getDataFilenames(self.dataDir)

        for filename in filenames:
            # 得到当前新闻类别
            cate = filename.split("&")[1][5:]
            print(filename)

            # 此处得到该excel文件夹所有信息，是一个list，list中单个元素为dict，对应 列名：值
            infoList = self.et.getExcelInfo(os.path.join(self.dataDir, filename))

            for new_info in infoList:
                urlstr = new_info["display_url"]
                # 区分链接，链接来自头条或新浪，关键词，toutiao.com和sina.com

                try:
                    # 这里需要去除sina的滚动图片类新闻及多媒体新闻
                    if urlstr.find("sina.com") != -1 and urlstr.find("slide") == -1 and urlstr.find("video") == -1:
                        print(urlstr)
                        textContent, htmlContent, img_url_list, keyword_list, abstract = self.ct.getSinaContent(urlstr)

                    elif urlstr.find("toutiao.com") != -1:
                        print(urlstr)
                        textContent, htmlContent, img_url_list = self.ct.getToutiaoContent(urlstr)

                    else:
                        continue
                except Exception as e:
                    continue

                if textContent == None:
                    continue

                 # 采用结巴中文分词提取正文最重要的十个特征词
                # 相关算法 --- tf-idf算法
                feature = jieba.analyse.extract_tags(textContent, 15)

                # 将当前新闻的关键词写入贝叶斯单词信息txt
                self.writeFeature(cate, feature)


    # cate为feature特征词集合所属的类别
    def writeFeature(self, cate, feature):
        self.fn.write(cate + ' ')
        for word in feature:
            if word not in self.word_ids:
                self.unique_words.append(word)
                # 使用unique_words当前数组长度作为单词的唯一id
                self.word_ids[word] = len(self.unique_words)

                #将单词与对应id写入单词：id字典文件
                self.fd.write(word + ' ' + str(self.word_ids[word]) + ' ')
            self.fn.write(str(self.word_ids[word]) + ' ')
        self.fn.write('#' + cate + '\n')

    def getDataFilenames(self,dir):
        fileList = []
        for dirpath, dirnames, filenames in os.walk(self.dataDir):
            break

        for filename in filenames:
            # 过滤非excel文件
            m = re.search(r"xlsx", filename)
            if not m:
                continue
            fileList.append(filename)
        return fileList

    def loadWord_id_dict(self):
        fd = open(dirPath + "/system/classPredict/NavieBayesInfo/word_id_dict.txt", 'r')
        allInfo = fd.read()
        arr = allInfo.strip().split()
        for i in range(0, len(arr)):
            if i % 2 == 0:
                self.word_ids[arr[i]] = arr[i + 1]
                if arr[i] not in self.unique_words:
                    self.unique_words.append(arr[i])

dp = DataPerpare(dirPath + "/system/classPredict/trainData")
dp.loadWord_id_dict()
dp.getNewContentAndAnalyse()
