# -*-coding:utf-8-*-
__author__ = 'howie'
import pymysql
#import sae.const
#import MySQLdb

admin = dict(
    WEBSITE=True,
    TOKEN="news&&admin"
)

#本地数据库配置
localDatabase = dict(
    localhost="127.0.0.1",
    database="howie",
    user="root",
    password="",
    charset="utf8",
    port=3306
)

#数据库连接,对应本地以及sae数据库连接配置
database = dict(
    #mysql for localhost
    localConn = pymysql.connect(host=localDatabase["localhost"],user=localDatabase["user"],passwd=localDatabase["password"],db=localDatabase["database"],port=localDatabase["port"],charset=localDatabase["charset"]),
    #mysql for sae
    #saeConn=MySQLdb.connect(host=sae.const.MYSQL_HOST,user=sae.const.MYSQL_USER,passwd=sae.const.MYSQL_PASS,db=sae.const.MYSQL_DB,port=3307,charset="utf8")

)
