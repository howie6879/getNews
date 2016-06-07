# -*- coding: utf-8 -*
__author__ = 'Howie,jeezy'

from config.n_conf import database

conn = database["localConn"]
cur = conn.cursor()


def select_table(table, column, condition, value):
    sql = "select " + column + " from " + table + " where " + condition + "= '" + value + "'"
    cur.execute(sql)
    lines = cur.fetchall()
    return lines


def insert_table(table, field, values):
    sql = "insert into " + table + field + " values" + values
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    return True

def update_column(table,column,value_set, condition,value_find):
    sql = "update " + table + " set " + column + "= '" + value_set + "' where " + condition + "='" + value_find  + "'"
    try:
        cur.execute (sql)
        conn.commit ()
    except:
        conn.rollback ()
    return True
    # result = select_table("user","name","name","howie")
    # print(result[0][0])
