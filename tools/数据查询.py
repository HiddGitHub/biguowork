# -*- coding:utf-8 -*-

import pymysql
import os


def get_account():
    userpath = os.path.expanduser("~")
    with open(userpath + "/sqlconfig", "r") as f:
        x = f.read()
    host, user, pwd = x.split("\n")

    return host, user, pwd


def toCon():
    try:
        host, user, pwd = get_account()
        # 打开数据库连接
        db = pymysql.connect(host=host, port=3306, database="biguoer", user=user, password=pwd, charset="utf8")
        return db
    except Exception as e:
        print("连接初始化失败", e)
        return


def sqlrun(sql):
    db = toCon()
    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    # 使用execute方法执行SQL语句

    try:
        # 执行sql语句
        cur.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        db.rollback()

    cur.close()
    db.close()

def selectrun(sql):
    db = toCon()
    # 使用cursor()方法获取操作游标
    cur = db.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:

            print(row)
            # id = row[0]
            # name = row[1]
            # sex = row[2]
            # age = row[3]
            # print(id, name, sex, age)
    finally:
        db.close()




if __name__ == '__main__':
    sql="""select * from `exams_real` where  `questionAsk` like '%组织承诺%' """
    selectrun(sql)
