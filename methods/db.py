#-*- coding: utf-8 -*
__author__ = 'Howie'

from config.n_conf import database

conn = database["localConn"]
cur = conn.cursor()

def select_table(table, column, condition, value ):
    sql = "select " + column + " from " + table + " where " + condition + "='" + value + "'"
    cur.execute(sql)
    lines = cur.fetchall()
    return lines



#result = select_table("user","name","name","howie")
#print(result[0][0])