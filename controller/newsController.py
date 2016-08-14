# -*-coding:utf-8-*-
__author__ = 'howie'
import os
from config.n_conf import dirPath

class NewsController():
    """
    系统控制类
    """

    def newsFiles(self, operator, sourceName):
        """
        :func   获取spider/sourceName/目录下爬取的各个新闻excel表
        :param  operator: 根据get或rm进行获取文件以及删除文件操作
                sourceName:新闻网站文件夹
        :return:获取文件操作返回文件名列表,删除文件,删除成功返回allFiles=False,表示目录下没有文件
        """
        # 获取新闻目录
        path = os.path.join(os.path.join(dirPath, 'spider'), sourceName)
        allFiles = []
        for dir in os.listdir(path):
            tarPath = os.path.join(path, dir)
            if os.path.isdir(tarPath):
                files = [file for file in os.listdir(tarPath) if
                        os.path.isfile(os.path.join(tarPath, file)) and os.path.splitext(file)[1] == ".xlsx"]
                if files and operator == "get":
                    for file in files:
                        allFiles.append(os.path.join(tarPath, file))
                # 删除原始数据
                elif files and operator == "rm":
                    for file in files:
                        os.remove(os.path.join(tarPath, file))
                        log = os.path.join(tarPath, file) + "文件删除成功"
                        print(log)
                        with open(dirPath+"/log.txt", 'a') as fp:
                            fp.write(log + "\n")
        if not allFiles:
            return False
        else:
            return allFiles

    def rmRepeate(self,*dirs):
        """
        func:       删除已经去重的文件
        :param *dirs:文件夹list,dirs[0]里面含有文件夹名称,默认为2个
        :return:    删除成功返回True
        """
        path = os.path.join(dirPath,'spider')
        #生成去重的数据目录
        for dir in dirs[0]:
            path = os.path.join(path,str(dir))

        files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path,file)) and os.path.splitext(file)[1] == ".xlsx"]
        for file in files:
            os.remove(os.path.join(path, file))
            log = os.path.join(path, file) + "文件删除成功"
            print(log)
            with open(dirPath+"/log.txt", 'a') as fp:
                fp.write(log + "\n")
        return True
