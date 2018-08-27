# -*- coding: utf-8 -*-
"""
Author  : yuqiuwang
Mail    : yuqiuwang929@gmail.com
Website : https://www.yuqiulearn.cn
Created : 2018/8/8 10:07
"""

import pymysql
import config

# --------------------------------------------------#
# 操作mysql数据库
# 提供了创建数据库、创建表、插入数据、查找数据、删除数据
# 通过main调用
# --------------------------------------------------#
#     main("create_db")
#     main("create_table")
#     main("insert_table", header, date, text, tag)
#     main("find_data", method, table_str, find_str)  # method = "all"/"one"/"ctn"
#     main("delete_data", table_str, find_str)
# --------------------------------------------------#
#


class CreateDB:
    def __init__(self, db, db_name):
        self.cursor = db.cursor()
        self.db_name = db_name

    def run_sql(self):
        sql = 'CREATE DATABASE %s' % self.db_name
        self.cursor.execute(sql)
        print("create database %s ok!" % self.db_name)


class CreateTable:

    def __init__(self, db, table_name, charset):
        self.cursor = db.cursor()
        self.table_name = table_name
        self.charset = charset

    def run_sql(self):
        self.cursor.execute("DROP TABLE IF EXISTS %s" % self.table_name)
        sql = """CREATE TABLE %s (
                 name_id INT NOT NULL AUTO_INCREMENT,
                 HEADER  CHAR(100),
                 DATE CHAR(10),
                 TEXT VARCHAR(6000),
                 TAG CHAR(20),
                 PRIMARY KEY(name_id))ENGINE=InnoDB DEFAULT CHARSET=%s;
                 """ % (self.table_name, self.charset)
        self.cursor.execute(sql)
        print("Created table %s!" % self.table_name)


class InsertTable:

    def __init__(self, db, table_name, header, date, text, tag):
        self.db = db
        self.cursor = db.cursor()
        self.my_dic = {"table": table_name, "header": header, "date": date, "text": text, "tag": tag}

    def run_sql(self):
        sql = """INSERT INTO {table}(HEADER, DATE, TEXT, TAG)
                 VALUES ('{header}', '{date}', '{text}', '{tag}')""".format(**self.my_dic)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("insert ok!")
        except:
            self.db.rollback()
            print("something wrong during insert!")


class FindData:

    def __init__(self, db, table_name, method, table_str, find_str):
        self.cursor = db.cursor()
        self.method = method
        self.my_dic = {"table": table_name, "table_str": table_str, "find_str": find_str}

    def run_sql(self):
        if self.method == "all":
            sql = "SELECT * FROM {table}".format(**self.my_dic)
        elif self.method == "one":
            sql = "SELECT * FROM {table} \
                    WHERE {table_str} = '{find_str}'".format(**self.my_dic)
        elif self.method == "ctn":
            sql = "SELECT * FROM {table} \
                    WHERE {table_str} LIKE '%{find_str}%'".format(**self.my_dic)
        try:
            out_puts = []
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                out_puts.append(list(row))
                print("find ok!")
        except:
            print("Error: unable to fetch data")
        return out_puts


class DeleteData:

    def __init__(self, db, table_name, table_str, find_str):
        self.db = db
        self.cursor = db.cursor()
        self.my_dic = {"table": table_name, "table_str": table_str, "find_str": find_str}

    def run_sql(self):
        sql = "DELETE FROM {table} \
                WHERE {table_str} = '{find_str}'".format(**self.my_dic)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Delete ok!")
        except:
            self.db.rollback()
            print("something wrong during delete!")


def main(command, *args):
    host = config.SqlConfig.host
    user = config.SqlConfig.user
    passwd = config.SqlConfig.passwd
    dbname = config.SqlConfig.dbname
    table_name = config.SqlConfig.table_name
    charset = config.SqlConfig.charset

    if command == "create_db":
        db = pymysql.connect(host, user, passwd, charset=charset)
        sql_type = CreateDB(db, dbname)
    else:
        db = pymysql.connect(host, user, passwd, dbname, charset=charset)
        if command == "create_table":
            sql_type = CreateTable(db, table_name, charset)
        elif command == "insert_table":
            header, date, text, tag = args
            sql_type = InsertTable(db, table_name, header, date, text, tag)
        elif command == "find_data":
            method, table_str, find_str = args
            sql_type = FindData(db, table_name, method, table_str, find_str)
        elif command == "delete_data":
            table_str, find_str = args
            sql_type = DeleteData(db, table_name, table_str, find_str)
        else:
            print("no command named %s" % command)
    result = sql_type.run_sql()

    db.close()
    return result

#main("create_db")
#main("create_table")
