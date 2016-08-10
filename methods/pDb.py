# -*- coding: utf-8 -*
__author__ = 'Howie,jeezy'

import pymysql
from config.n_conf import localDatabase


class newsDb(object):
    """
    connect mysql
    """

    def __init__(self):
        self.conn = pymysql.connect(**localDatabase)
        self.cur = self.conn.cursor()

    def select_table(self, table, column, condition, value):
        sql = "select " + column + " from " + table + " where " + condition + "= '" + value + "'"
        print(sql)
        self.cur.execute(sql)
        lines = self.cur.fetchall()
        return lines

    def select_table_two(self, table, column):
        sql = "select " + column + " from " + table
        print (sql)
        self.cur.execute (sql)
        lines = self.cur.fetchall ()
        return lines

    def select_table_three(self,sql):
        print (sql)
        self.cur.execute (sql)
        lines = self.cur.fetchall ()
        return lines

    def  insert_table(self, table, field, values):
        sql = "insert into " + table + field + " values" + values
        print(sql)
        try:
            self.cur.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            return True
        except:
            # 出现错误则回滚
            self.conn.rollback()
            return False

    def update_column(self, table, column, value_set, condition, value_find):
        sql = "update " + table + " set " + column + "= '" + value_set + "' where " + condition + "='" + value_find + "'"
        print(sql)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False



    def exeSql(self,sql):
        print (sql)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def __del__(self):
        self.cur.close()
        self.conn.close()
