
import jieba
import jieba.analyse
import os
import re
from wordAna.contentTool import  ContentOperator
from wordAna.excelTool import ExcelOperator

def getNewsContent(newsDir,category,address="toutiao.com"):
    """
    :param category:目录名
    :param newsDir: 对应网站新闻存放的总目录，比如toutiaoSource
    :param address:网站链接中固有的特征，比如头条网的toutiao.com
                    以参数传递，才能让新浪和头条共用
    :return:
    """
    #获取总目录绝对路径
    orgDir = os.path.abspath(".")+"/"+ newsDir + "/"
    #获取最终存放目录绝对路径
    finalDir = os.path.abspath(".") +"/" +  "finalSource/"
    print(finalDir)

    #获得excelTools.py中的excel操作工具
    et = ExcelOperator()
    #获得contentTools.py中的content操作工具
    ct = ContentOperator()

    for i in range(len(category)):
        typeDir = orgDir + category[i] + "/"
        finalTypeDir = finalDir + category[i]
        print(typeDir)
        for parent,dirnames,filenames in os.walk(typeDir):
            print(dirnames)
            if not os.path.exists(finalTypeDir):
                os.mkdir(finalTypeDir)
            #开始遍历各大新闻类别文件夹下的excel文件
            for filename in filenames:
                print(filename)
                m = re.search(r"xlsx",filename)
                if not m:
                    continue
                #此处得到该excel文件夹所有信息，是一个list，list中单个元素为dict，对应 列名：值
                infoList = et.getExcelInfo(os.path.join(typeDir,filename))

                #用以存放完整的新闻信息元素的集合
                last_list = []
                for new_info in infoList:
                    urlstr = new_info["display_url"]
                    #该链接指向网站本身，比如链接中含有toutiao.com表示该链接表示的新闻来自头条
                    if urlstr.find( address ) != -1:
                        textContent,htmlContent = ct.getContent(urlstr)
                        #采用结巴中文分词提取正文最重要的十个特征词
                        #相关算法 --- tf-idf算法
                        feature = jieba.analyse.extract_tags(textContent,10)
                        new_info["textContent"] = textContent
                        new_info["htmlContent"] = htmlContent
                        new_info["feature"] = feature
                        last_list.append(new_info)

                #信息过滤、爬取及关键词提取完毕，开始将它存到excel表中
                excelName = finalTypeDir + "/" + filename
                #？？？？这里，第二个参数，工作表名称，需调整
                et.saveToExcel(excelName,"toutiao",last_list)


#新闻种类
category = ["__all__", "news_hot", "video", "gallery_detail", "news_society", "news_entertainment",
            "news_tech", "news_car", "news_sports", "news_finance", "news_military", "news_world",
            "news_fashion", "news_travel", "news_discovery", "news_baby", "news_regimen", "news_story",
            "news_essay", "news_game", "news_history", "news_food", ]