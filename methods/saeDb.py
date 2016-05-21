#-*- coding: utf-8 -*
__author__ = 'Howie'
import sae.const
import MySQLdb

conn=MySQLdb.connect(host=sae.const.MYSQL_HOST,user=sae.const.MYSQL_USER,passwd=sae.const.MYSQL_PASS,db=sae.const.MYSQL_DB,port=3307,charset="utf8")
cur = conn.cursor()

def select_table(table, column, condition, value ):
    sql = "select " + column + " from " + table + " where " + condition + "='" + value + "'"
    cur.execute(sql)
    lines = cur.fetchall()
    return lines

#result = select_table("user","name","name","howie")
#print(result[0][0])