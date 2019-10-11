# -*- coding:utf-8 -*-

import xlrd
import random
import xlwt
import os
import re
import time
import requests
from lxml import etree


def generatePname():  # 根据时间戳和随机字母生成不重复的链接用于替换旧链接
    pName = str("{:.7f}".format(time.time()))
    a = chr(random.randrange(65, 65 + 26))
    b = chr(random.randrange(65, 65 + 26))
    c = chr(random.randrange(65, 65 + 26))
    d = chr(random.randrange(65, 65 + 26))
    pName = pName.replace(".", a + b + c + d)

    return pName


# print(generatePname())
def toSaveImg(oneArry, sPath):  # 遍历 找出链接替换并下载
    # if not os.path.exists(sPath):
    #     os.makedirs(sPath)
    for n in range(2, len(oneArry)):
        if oneArry[n] == "":
            continue
        else:
            try:
                if not re.findall(r"<img|<IMG", oneArry[n]):
                    srcStr = re.sub(r"<.*?>", "  ", oneArry[n])
                    oneArry[n] = srcStr
                    continue
                mystrs = changeSrc(oneArry[n], sPath)
                if mystrs != "":
                    oneArry[n] = mystrs

            except Exception as e:
                print("my err", e)
                continue

    return oneArry


alldic = {}


def ral_m(m):
    newM = m.replace(r"\/", "/")

    if re.findall(r"\/(\d+)\/images\/.*", newM):
        get0 = re.findall(r"\/(\d+)\/images\/(.*)", newM)
        newM = 'https://img.examcoo.com/paper/' + get0[0][0] + '/' + get0[0][1]
    # print(newM+"\n")
    return newM


# ral_m("uploads/3/100461/images/201012/02163058.jpg")

def changeSrc(srcStr, pPath):  # 带图片的字符串    存储路径
    global alldic  # 全局变量 用于匹配是否已经存在的题目

    if not pPath.endswith("/"):
        pPath = pPath + "/"
    srcStr = srcStr.replace('<IMG', "<img")

    # 针对考试酷
    # print(srcStr)
    # srcStr = re.sub(r"src=", r"saarc=", srcStr)
    # srcStr = re.sub(r"_djrealurl=", r"src=", srcStr)

    # ========

    if not re.findall(r"<img", srcStr):
        srcStr = re.sub(r"<.*?>", " ", srcStr)
        # print(srcStr)
    if re.findall(r"<img.*?src=[\"\'](.*?)[\"\'].*?>", srcStr):
        print(srcStr)
        srcStr = re.sub(r"(<img).*?(src=[\"\'](.*?)[\"\']).*?>", r"\1 \2 />", srcStr)
        # print("    old src###",srcStr)
        # srcStr = re.sub(r"title=[\"\'].*?[\"\']","",srcStr)
        # srcStr = re.sub(r"alt=[\"\'].*?[\"\']","",srcStr)
        needpath = re.findall(r"<img.*?src=[\"\'](.*?)[\"\'].*?>", srcStr)
        print("sssssss", needpath)
        for m in needpath:
            # needM = ral_m(m)
            needM = m
            if needM not in alldic.keys():

                newName = generatePname()
                newName = newName + ".jpg"
                newPath = "https://file.biguotk.com/img/topic/" + newName
                alldic[needM] = newPath
                # print(" old",srcStr)
                #  下载地址 ，部分时候需要拼接链接
                # needM = ral_m(m)
                # needM=m
                if not os.path.exists(pPath):
                    os.makedirs(pPath)
                downPhoto(needM, pPath+newName)
                time.sleep(0.05)
                m = re.sub("\?", "\?", m)
                m = re.sub("\|", "\|", m)
                m = re.sub(r"\\", r"\\", m)
                m = re.sub(r"\/", r"\/", m)
                srcStr = re.sub(m, newPath, srcStr)  # 替换img  里的 src url
            else:
                print("已有无需再次下载")
                m = re.sub("\?", "\?", m)
                m = re.sub("\|", "\|", m)
                m = re.sub(r"\\", r"\\", m)
                m = re.sub(r"\/", r"\/", m)
                srcStr = re.sub(m, alldic[needM], srcStr)
            # print(" newstr",srcStr)
        # print("down over",srcStr)
        return srcStr

    else:
        return ""


# s = requests.session()
def downPhoto(url, savePath):  # 下载图片  并存储


    headers = {

        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        # "referer": "https://www.examcoo.com/editor/do/recur/id/72534238/tokenleid/90c7ebfc751b2066fd3bef458c0b9245",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    res = requests.get(url, headers=headers, verify=False,timeout=8)
    if int(res.status_code) < 400:
        with open(savePath, mode="wb") as f:
            f.write(res.content)
            f.flush()
        # print("====ok save",savePath)
        print("down over", savePath)
        return 1
    else:
        print("the img is errp", res.status_code)
        return -1


def get_xpath(html):  # 获取文本和部分html 转换出所需的部分
    content2 = etree.tostring(html).decode("utf8")
    content2 = get_chainese(content2)
    # print("content2",content2)

    # 去除非img的标签
    if not re.finditer(r"<img.*?>", content2):
        content2 = re.sub(r"<.*?>", "", content2)
    else:
        cli = re.findall(r"<img.*?>", content2)
        n = 0
        for c in cli:
            content2 = re.sub(c, "#_#" + str(n), content2)
            n += 1

        content2 = re.sub(r"<.*?>", "", content2)
        nn = 0
        for c in cli:
            content2 = re.sub("#_#" + str(nn), c, content2)
            nn += 1

    return content2


def isHave(name):
    oldpaper = open("./zhentiPaper", mode="r", encoding='utf8')
    lines = oldpaper.readlines()
    # print(lines)
    oldpaper.close()

    for line in lines:
        if name + "\n" == line:
            print("已存在==", name)
            return -1

        elif name + "\n" != line and line == lines[-1]:
            print("不存在", name)
            return 1


def get_chainese(strs):  # 将对应的数字转换成中文
    regex = re.compile('&#(\d+);')

    matchs = regex.findall(strs)

    for i in matchs:
        strs = strs.replace('&#%s;' % i, chr(int(i)))

    return strs


def getAllArry():
    paper_array = [['序号', '类型', '问题', '选项A', '选项B', '选项C', '选项D', '选项E', '选项F', '正确答案', '解释']]
    return paper_array


def getOneArry():
    array = []
    for i in range(1, 12):
        array.append('')
    return array


def write_xlsx(fpath, fname, con_list):  # 参数：('C:\work/',"2010年10月真题",conlist)
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Tahoma'
    font.bold = False
    font.italic = False
    font.underline = False
    style.font = font
    if not os.path.exists(fpath):  # fname 为没有后缀名的
        os.makedirs(fpath)
    if not fpath.endswith("/"):  # 让fpath 是否带/都可以通过
        fpath = fpath + "/"
    filename = fname + '.xls'
    path = os.path.join(fpath, filename)
    if os.path.exists(path):
        os.remove(path)
    try:
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        for i in range(len(con_list)):
            for j in range(0, 11):
                worksheet.write(i, j, con_list[i][j])

        workbook.save(path)
        print('写入<%s>excel完毕!' % fname)
    except Exception as e:
        print(e)


def sendEmail(message):
    import smtplib
    from email.mime.text import MIMEText
    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = "18879662543@163.com"  # 用户名
    mail_pass = "qiull123456"  # 授权密码，非登录密码
    sender = "18879662543@163.com"
    receivers = ["550719255@qq.com"]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    title = 'Message from Spider'  # 邮件主题
    message = MIMEText(message, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("Email Seed Successfully.")
    except smtplib.SMTPException as e:
        print("send email err", e)


def setTimer(func, setTime="00:00"):
    while True:
        needTime = time.strftime("%H:%M")
        if needTime == setTime:
            print("start======")
            func()
            time.sleep(60)


def change(num):
    num = int(num)
    if num == 0:
        return "A"
    elif num == 1:
        return "B"
    elif num == 2:
        return "C"
    elif num == 3:
        return "D"
    elif num == 4:
        return "E"
    elif num == 5:
        return "F"


class HowManyExcel:
    def __init__(self, path):

        self.path = path
        self.num = 0
        if os.path.isdir(self.path):
            self.run(self.path)
            # print(self.num)
        print(self.num)
        # return self.num

    def run(self, newpath):  # self.path is a dir

        if os.path.isdir(newpath):
            dli = os.listdir(newpath)
            for a in dli:
                newpath2 = os.path.join(newpath, a)
                # print(newpath)
                if newpath2.endswith(".xlsx"):
                    self.num += 1
                if os.path.isdir(newpath2):
                    self.run(newpath2)

    def getNum(self):
        return self.num



def do(basepath):
    pli = os.listdir(basepath)

    # rdel=[]
    rdel1={}
    nnn=1
    for new in pli:
        print(new)

        try:
            if new=='.DS_Store':
                continue
            newpath = os.path.join(basepath,new)
            wb = xlrd.open_workbook(newpath)
            sheet = wb.sheet_by_index(0)
            que_col = sheet.col(2)
            cls2=[]
            errcls=[]
            other=[]
            for i in range(1,len(que_col)):
                # print(i)

                try:
                    que = str(sheet.row(i)[2].value)
                    # print(que)

                    toread =que
                    cls = int(sheet.row(i)[1].value)
                    # print(cls)
                    ans = str(sheet.row(i)[9].value)
                    any = str(sheet.row(i)[10].value)
                    que =que.replace("&emsp;"," ").replace("\xa0"," ").replace("\u3000"," ").replace("&nbsp;"," ")

                    que =re.sub(r" {1,20}"," ",que)
                    que =re.sub(r" {0,19}[【\(（] {0,20}[】\)）] {0,5}","",que)
                    que = re.sub(r"^ {1,10}","",que)
                    que = re.sub(r"^(<.*?>) {1,10}",r"",que)
                    que = re.sub(r"<.*?>",r"",que)
                    que = re.sub(r"[【\(（]{0,1} {0,20}名词解释 {0,20}[】\)）]{0,1}[：:]{0,1}", r"", que)
                    que = re.sub(r"[【\(（]{0,1} {0,20}单选题 {0,20}[】\)）]{0,1}[：:]{0,1}", r"", que)
                    que = re.sub(r"[【\(（]{0,1} {0,20}单项选择题 {0,20}[】\)）]{0,1}[：:]{0,1}", r"", que)
                    que = re.sub(r"[【\(（]{0,1} {0,20}多项选择题 {0,20}[】\)）]{0,1}[：:]{0,1}", r"", que)
                    que = re.sub(r"[【\(（]{0,1} {0,20}多选题 {0,20}[】\)）]{0,1}[：:]{0,1}", r"", que)
                    que = re.sub(r"[【\(（]{0,1} {0,20}简答题 {0,20}[】\)）]{0,1} {0,1}", r"", que)
                    que=que.replace('.',"").replace('，',"").replace('。',"").replace('？',"").replace('?',"").replace(',',"").replace('"',"").replace('：',"").replace('、',"").replace('_',"")
                    chose_a = str(sheet.row(i)[3].value)

                    chose_a =re.sub(r"<.*?>",r"",chose_a).replace('.',"").replace('，',"").replace('。',"").replace('？',"").replace('?',"").replace(',',"").replace('"',"").replace('：',"").replace('、',"")


                    chose_b = str(sheet.row(i)[4].value)
                    chose_d = str(sheet.row(i)[6].value)
                    oneredel = que + str(chose_a)

                    if cls==1 or cls==2 or cls==3 or ans=='' or ans=='模考':
                        ans1 = re.sub('<.*?>', '', ans)
                        if (ans=='' and any=="") or ans=='模考' or ans=="正确" or ans=='错误':
                            errcls.append(toread)

                            rdel1[oneredel] = 1
                            # print('=======', nnn)
                            # print()
                            # print('ans err',toread.replace("\n",''))
                            # nnn += 1

                            continue
                        if cls==1 or cls==2 or cls==3:
                            if (chose_d == "" and chose_b == "" ) or chose_a=="" or chose_b=="":
                                # oneredel = que + str(chose_a)
                                errcls.append(toread)
                                rdel1[oneredel] = 1
                                # print('=======', nnn)
                                # print()
                                # print('ans err', toread.replace("\n", ''))
                                # nnn += 1

                                continue


                        if (cls==1 and len(ans1)>1) or (cls==2 and len(ans1)==1):
                            errcls.append(toread)
                            rdel1[oneredel] = 1

                            # print('=======', nnn)
                            # print()
                            # print([ans1])
                            # print("type chose ", toread.replace("\n", ''))
                            # nnn += 1

                            continue
                    elif cls==4:
                        if ans=='A' or ans=='B' or ans=="正确" or ans=='错误':
                            errcls.append(toread)
                            rdel1[oneredel] = 1

                            # print('=======', nnn)
                            # print()
                            # print("cls err", toread.replace("\n", ''))
                            # nnn += 1

                            continue



                    # print(oneredel)
                    if oneredel  in rdel1.keys():
                        if rdel1[oneredel]==1:
                            # print('=======',nnn)
                            if cls ==2:
                                cls2.append(toread)
                                rdel1[oneredel] = 2

                            else:
                                other.append(toread.replace("\n",''))
                                # print('=======', nnn)
                                # print()
                                # print(toread.replace("\n",''))
                                # rdel1[oneredel]=2
                                # nnn+=1

                                pass
                        elif rdel1[oneredel]==2:

                            continue
                    # rdel.append(oneredel)
                    else:
                        rdel1[oneredel]=1

                except Exception as e:

                    print('err',sheet.row(i)[2].value,e)
                    continue

            print()
            print("==============多选重复=============")
            print()

            for one in cls2:
                print('cls2============', nnn)
                print()
                print(one.replace("\n", ''))
                # rdel1[one] = 2
                nnn += 1

                pass
            print()
            print("==============错误题目=============")
            print()
            for one in errcls:
                print('err===========', nnn)
                print()
                print(one.replace("\n", ''))
                # rdel1[one] = 2
                nnn += 1

                pass
            print()
            print("==============重复题=============")
            print()
            for one in other:
                print('===========', nnn)
                print()
                print(one.replace("\n", ''))
                # rdel1[one] = 2
                nnn += 1

                pass
        except:
            print(1)
            continue


if __name__ == '__main__':

    baurl =r'/Users/qiu60/Desktop/safariDown'
    do(baurl)  #第一个文件题目数量  文件个数

















