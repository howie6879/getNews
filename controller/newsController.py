# -*-coding:utf-8-*-
__author__ = 'howie'
import os


class NewsController():
    """
    系统控制类
    """
    def __init__(self):
        pass

    def touTiaoFiles(self, operator):
        """
        :func   获取spider/source/目录下爬取的各个新闻excel表
        :param  operator: 根据get或rm进行获取文件以及删除文件操作
        :return:获取文件操作返回文件名列表,删除文件,删除成功返回allFiles=False,表示目录下没有文件
        """
        # 获取主路径
        path = os.path.dirname(os.path.abspath('.'))
        # 获取新闻目录
        path = os.path.join(os.path.join(path, 'spider'), 'source')
        allFiles = []
        for dir in os.listdir(path):
            dirPath = os.path.join(path, dir)
            if os.path.isdir(dirPath):
                file = [file for file in os.listdir(dirPath) if
                        os.path.isfile(os.path.join(dirPath, file)) and os.path.splitext(file)[1] == ".xlsx"]
                if file and operator == "get":
                    for f in file:
                        allFiles.append(os.path.join(dirPath, f))
                elif file and operator == "rm":
                    for f in file:
                        os.remove(os.path.join(dirPath, f))
                        log = os.path.join(dirPath, f)+"文件删除成功"
                        print(log)
                        with open("../spider/log.txt", 'a') as fp:
                            fp.write(log + "\n")
        if not allFiles: return False
        else:return allFiles
# NewsController = NewsController()
# print(NewsController.touTiaoFiles("get"))