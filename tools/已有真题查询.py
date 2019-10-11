# coding:utf-8
import pymysql
import os
import datetime as dtf,time


class Filter():
    def __init__(self):
        try:
            host,user,pwd = self.get_account()
            self.db = pymysql.connect(host=host,port=3306,database="biguoer",user=user,password=pwd,charset="utf8")
        except Exception as e:
            print("连接初始化失败",e)
            return
        self.create_list()
        # self.result = self.check()

    def create_list(self):
        try:
            cs = self.db.cursor()
            count = cs.execute("SELECT b.`year`,b.`month`,a.`name` FROM (SELECT NAME,CODE FROM courses GROUP BY `code`) as a RIGHT JOIN exams_real_paper as b ON a.code = b.`code`")
            # print(count)
            self.result = cs.fetchall()
            li = list(set(self.result))
            li1 = []
            for i,j,k in li:
                z = str(i) + "_" + str(j) + "_" + str(k).strip().replace("(","").replace(")","").replace(" ","").replace("（","").replace("）","")
                li1.append(z)
            print("len li1 = ",len(li1))
            # li1.append(str(dtf.datetime.now())[:-7])
            content = "\n".join(li1)
            cs.close()
            self.db.close()
            with open("zhentiPaper","w",encoding="utf8") as f:
                f.write(content)
                f.flush()
        except Exception as e:
            print("数据查询出错:",e)
            self.db.close()
            li1 = ["2017-12-30 00:00:00"]
        return li1

    # def update(self):
    #     li = self.create_list()
    #     return li

    @staticmethod
    def get_account():
        userpath = os.path.expanduser("~")
        with open(userpath + "/sqlconfig", "r") as f:
            x = f.read()
        host, user, pwd = x.split("\n")
        print(host,user,pwd)
        return host, user, pwd

    # def check(self):
    #     ntime = dtf.datetime.now()
        # if not os.path.exists("./zhentiPaper"):
        # self.create_list()
        # else:
        #     with open("./zhentiPaper","r",encoding="utf8") as f:
        #         li = f.readlines()
        #     if len(li) > 0:
        #         st = li[-1]
        #         ct = dtf.datetime.strptime(st,"%Y-%m-%d %H:%M:%S")
        #     else:
        #         print("未获取到paperlist的内容")
        #         li = self.create_list()
        #         ct = ntime
        #     if ct + dtf.timedelta(hours=12)<ntime:
        #         li = self.update()
        # return li[:-1]




if __name__ == '__main__':
    Filter()
    # print(existpapers)
