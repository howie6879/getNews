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
    files = [x for x in os.listdir(orgDir) if os.path.splitext(x)[-1] == '.xlsx']

    # 开始遍历各大新闻类别的excel文件
    for file in files:
        # print(file)
        # 此处得到该excel文件夹所有信息，是一个list，list中单个元素为dict，对应 列名：值
        infoList = et.getExcelInfo(os.path.join(orgDir, file))
        # 用以存放完整的新闻信息元素的集合
        last_list = []
        for new_info in infoList:
            urlstr = new_info["display_url"]
            # 区分链接，链接来自头条或新浪，关键词，toutiao.com和sina.com
            htmlContent, textContent, title, abstract, keywords, source, tag = '', '', '', '', '', '', ''
            img_url_list = []
            try:
                # 这里需要去除sina的滚动图片类新闻及多媒体新闻
                if urlstr.find("sina.com") != -1 and urlstr.find("slide") == -1 and urlstr.find("video") == -1:
                    print(urlstr)
                    textContent, htmlContent, img_url_list, keyword_list, abstract = ct.getSinaContent(urlstr)
                    new_info["keywords"] = ' '.join(keyword_list)
                    new_info["abstract"] = ' '.join(abstract)

                elif urlstr.find("toutiao.com") != -1:
                    print(urlstr)
                    textContent, htmlContent, img_url_list, title, abstract, keywords, source, tag = ct.getToutiaoContent(
                        urlstr)
                    if title:
                        new_info["title"] = title
                    else:
                        new_info["title"] = ''
                    if abstract:
                        new_info["abstract"] = abstract
                    else:
                        new_info["abstract"] = ''
                    if keywords:
                        new_info["keywords"] = keywords
                    else:
                        new_info["keywords"] = ''
                    if source:
                        new_info["source"] = source
                    else:
                        new_info["source"] = ''
                    if tag:
                        new_info["tag"] = tag
                    else:
                        new_info["tag"] = ''
            except:
                pass
                # 采用结巴中文分词提取正文最重要的十个特征词
                # 相关算法 --- tf-idf算法
                # print(textContent)
            try:
                feature = jieba.analyse.extract_tags(textContent, 15)
                new_info["textContent"] = textContent
                new_info["htmlContent"] = htmlContent
                new_info["feature"] = feature
                new_info["img"] = img_url_list
                last_list.append(new_info)
            except:
                pass

        # 信息过滤、爬取及关键词提取完毕，开始将它存到excel表中
        excelName = os.path.join(finalDir, file)
        print("excelName:" + excelName)
        # 这里，第二个参数，工作表名称，需调整
        et.saveToExcel(excelName, "allNews", last_list)
