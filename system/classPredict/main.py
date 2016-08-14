import pymysql
import os
from system.classPredict.newsPredict import NewPredict
from system.classPredict.predictTool import NavieBayesPredict
from methods.pDb import newsDb
from config.n_conf import dirPath

# 存放新闻信息的集合，包括 id,文本正文
data_list = []

test_data_file = dirPath + "/system/classPredict/NavieBayesInfo/predict_new_word.txt"
model_file = dirPath + "/system/classPredict/NavieBayesInfo/model.txt"
result_file = dirPath + "/system/classPredict/NavieBayesInfo/predict_result.txt"


def startPredict():
    db = newsDb()

    try:
        datasql = "select news_id,text_content from get_news where is_old = 0"
        data = db.select_table_three(datasql)
        for d in data:
            new = {}
            new["id"] = d[0]
            new["textContent"] = d[1]
            data_list.append(new)

    except Exception as e:
        print(e)

    np = NewPredict(data_list)
    np.getNewInfo()
    nb = NavieBayesPredict(test_data_file, model_file, result_file)
    nb.predict()

    # startPredict()
