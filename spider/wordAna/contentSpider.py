import jieba
import jieba.analyse
import os
import re
from spider.wordAna.contentTool import ContentOperator
from spider.wordAna.excelTool import ExcelOperator


def getNewsContent():
    """
    :return:
    """
    # 获取总目录绝对路径
    orgDir = os.getcwd() + "/spider/wordAna/allNews"
    # 获取最终存放目录绝对路径
    finalDir = os.getcwd() + "/spider/wordAna/wordAnaNews/"
    print(orgDir)
    print(finalDir)

    # 获得excelTools.py中的excel操作工具
    et = ExcelOperator()
    # 获得contentTools.py中的content操作工具
    ct = ContentOperator()

    for dirpath, dirnames, filenames in os.walk(orgDir):
        break

    global textContent
    global htmlContent
    global img_url_list
    # 开始遍历各大新闻类别的excel文件
    for filename in filenames:

        m = re.search(r"xlsx", filename)
        if not m:
            continue

        print(filename)
        # 此处得到该excel文件夹所有信息，是一个list，list中单个元素为dict，对应 列名：值
        infoList = et.getExcelInfo(os.path.join(dirpath, filename))
        # 用以存放完整的新闻信息元素的集合
        last_list = []
        for new_info in infoList:
            urlstr = new_info["display_url"]
            # 区分链接，链接来自头条或新浪，关键词，toutiao.com和sina.com

            try:
                # 这里需要去除sina的滚动图片类新闻及多媒体新闻
                if urlstr.find("sina.com") != -1 and urlstr.find("slide") == -1 and urlstr.find("video") == -1:
                    print(urlstr)
                    textContent, htmlContent, img_url_list, keyword_list, abstract = ct.getSinaContent(urlstr)
                    new_info["keywords"] = ' '.join(keyword_list)
                    new_info["abstract"] = ' '.join(abstract)

                elif urlstr.find("toutiao.com") != -1:
                    print(urlstr)
                    textContent, htmlContent, img_url_list = ct.getToutiaoContent(urlstr)
                else:
                    continue
            except:
                continue

            if textContent == None or htmlContent == None:
                continue

            # 采用结巴中文分词提取正文最重要的十个特征词
            # 相关算法 --- tf-idf算法
            feature = jieba.analyse.extract_tags(textContent, 10)
            new_info["textContent"] = textContent
            new_info["htmlContent"] = htmlContent
            new_info["feature"] = feature
            new_info["img"] = img_url_list
            last_list.append(new_info)

            # 信息过滤、爬取及关键词提取完毕，开始将它存到excel表中
        excelName = os.path.join(finalDir, filename)
        print("excelName:" + excelName)
        # 这里，第二个参数，工作表名称，需调整
        et.saveToExcel(excelName, "allNews", last_list)
