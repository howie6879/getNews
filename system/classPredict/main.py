import pymysql
import os
from system.classPredict.newsPredict import NewPredict
from system.classPredict.predictTool import NavieBayesPredict
import methods.db as db



#存放新闻信息的集合，包括 id,文本正文
data_list = []

test_data_file = "system/classPredict/NavieBayesInfo/predict_new_word.txt"
model_file = "system/classPredict/NavieBayesInfo/model.txt"
result_file = "system/classPredict/NavieBayesInfo/predict_result.txt"

def startPredict():
    db.cur.execute("delete from news_tag_deep")
    db.conn.commit()
    try:

        db.cur.execute('select news_id,text_content from get_news where is_old=0')
        data = db.cur.fetchall()

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

#startPredict()