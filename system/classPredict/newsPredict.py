
import os
import jieba
import jieba.analyse
from config.n_conf import dirPath


class NewPredict(object):
    def __init__(self,data_list):
        self.data_list = data_list

        self.ft = open(dirPath + "/system/classPredict/NavieBayesInfo/predict_new_word.txt", 'w')
        #存放 单词：对应唯一id 的字典
        self.word_id_dict = {}
        #加载单词id字典，结果在word_id_dict里
        self.loadWord_id_dict()


    #将所需预测的新闻的类别：特征词保存进文件，格式： 类别 单词1id  单词2id  单词3id....... #
    def getNewInfo(self):
        for new in self.data_list:

            new_id = new["id"]

            textContent = new["textContent"]
            if textContent==None:
                continue

            feature = jieba.analyse.extract_tags(textContent, 15)
            # print(new_id + " " + str(feature))
            #代表当前新闻的特征词id集合
            word_id_list = []
            for word in feature:
                tmp = self.word_id_dict.get(word, None)
                if tmp==None:
                    word_id_list.append("-1")
                else:
                    word_id_list.append(str(tmp))

            #将文章信息写入预测新闻信息文件
            self.writeFeature(new_id, word_id_list)
        #关闭资源
        self.ft.close()

    # cate为feature特征词id集合所属的类别
    def writeFeature(self, new_id, word_id_list):
        self.ft.write(new_id + ' ')
        for word_id in word_id_list:
            self.ft.write(word_id + ' ')
        self.ft.write('\n')


    def loadWord_id_dict(self):
        fd = open (dirPath + "/system/classPredict/NavieBayesInfo/word_id_dict.txt", 'r')
        allInfo = fd.read()
        arr = allInfo.strip().split()
        for i in range(0,len(arr)):
            if i%2==0:
                self.word_id_dict[arr[i]] = arr[i+1]


# np = NewPredict([])
# np.loadWord_id_dict()
