import pyperclip
import requests
import json
from urllib import parse
import Exceptions
from selenium import webdriver
from PIL import ImageGrab
from aip import AipOcr
import getter
from win32api import MessageBox
from win32con import MB_OK
import time
import re
import configparser
import _thread
import threading


__header = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Authorization': ""
}

__token = "3d0da4a49407f37445a667768ff8f4ab"


def Output(message):
    # MessageBox(0, message, "答案", MB_OK)
    print(message)


# clip = pyperclip.paste()

def getDataOCR(aipOcr):
    img1 = ImageGrab.grabclipboard()
    if img1 is None:
        raise Exceptions.ClipNotIMG("剪切板不是图片")
    # print(type(img))
    # 文件保存的名字
    img_path = '1.png'
    # 保存图片
    img1.save(img_path)
    # 百度api执行所需数据，运行需换成自己的APP_ID，API_KEY，SECRET_KEY

    with open(img_path, 'rb') as f:
        img2 = f.read()
        f.close()
    # print(type(img2))
    # 识别图片并返回结果
    result = aipOcr.basicAccurate(img2)

    data = ''
    for r in result['words_result']:
        data = data + r['words'] + '\n'
    return data

def getDataPaste(last):
    tmp = pyperclip.paste()
    if tmp == last:
        return ""
    return tmp

def getFromBaidu(question):
    b = webdriver.Chrome()
    b.get("https://www.baidu.com/s?wd=" + tmp)
    b.find_element_by_id("kw").send_keys(question)
    b.find_element_by_id("su").click()

def findAnswer(a, th):
    courseid = "206267220"
    g = getter.getter()
    str = ""
    j = ['I', 'II', 'III', 'IV']
    h = 0
    try:
        tmp = g.get({'q': a, 'curs': courseid, 'type': "1", 'token': __token})
    except Exceptions.NoAnswerFound:
        # To Do List
        # 递归 findAnswer(a,times)
        # 削减文字内容重新查找
        getFromBaidu(a)
    except ConnectionError:
        return "连接出错"
    else:
        for i in tmp:
            if i['answer'] == "":
                continue
            str += j[h] + ". : " + "\n" + i['answer'] + "\n"
            str += '-' * 20
            str += "\n"
            h += 1
    Output(th+str)

def theardSearch(cfg, start, end, th):
    loop = 1
    for i in cfg.sections():
        if loop - start < 0:
            loop += 1
            continue
        if loop > end:
            break
        print(cfg.get(i, "tm"))
        findAnswer(cfg.get(i, "tm"),th)

        loop += 1


def textProcess(text):
    tmpS = text
    tmpS = tmpS.strip()
    tmpS = tmpS.replace(" ", '')
    tmpS = tmpS.replace("\n", '')
    tmpS = tmpS.replace("\t", '')
    tmpS = tmpS.replace("\r", '')
    tmpS = tmpS.replace("\xa0", '')
    tmpS = tmpS.replace("\x20", '')
    tmpS = tmpS.replace("\u3000", '')
    return tmpS

# 初始化题目文件
cfg1 = configparser.ConfigParser()
cfg1.read("question.ini",encoding="utf-8")

num = int((cfg1.sections().__len__() - int(cfg1.sections().__len__() % 8))/8)
start = time.time()
th1 = threading.Thread(target=theardSearch,args=(cfg1,1,num,"th1:"))
th2 = threading.Thread(target=theardSearch,args=(cfg1,num+1,num*2,"th2:"))
th3 = threading.Thread(target=theardSearch,args=(cfg1,num*2+1,num*3,"th3:"))
th4 = threading.Thread(target=theardSearch,args=(cfg1,num*3+1,num*4,"th4:"))
th5 = threading.Thread(target=theardSearch,args=(cfg1,num*4+1,num*5,"th5:"))
th6 = threading.Thread(target=theardSearch,args=(cfg1,num*5+1,num*6,"th6:"))
th7 = threading.Thread(target=theardSearch,args=(cfg1,num*6+1,num*7,"th7:"))
th8 = threading.Thread(target=theardSearch,args=(cfg1,num*7+1,int(cfg1.sections().__len__()),"th8:"))
th1.start()
th2.start()
th3.start()
th4.start()
th5.start()
th6.start()
th7.start()
th8.start()
th1.join()
th2.join()
th3.join()
th4.join()
th5.join()
th6.join()
th7.join()
th8.join()
end = time.time()
print(end-start)
quit()
last_string = pyperclip.paste()
APP_ID = '19124804'
API_KEY = 'cCMaB793Gff1w6yE9HojaE4z'
SECRET_KEY = 'PMMOEcom53RHgXpwXfoHObilbf4V3oQe'
# 初始化AipOcr
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
tmp = ""
baiduAPI = True

while True:
    if baiduAPI:
        try:
            tmp = getDataOCR(aipOcr)
        except Exceptions.ClipNotIMG:
            tmp = getDataPaste("")
        except:
            continue
    else:
        tmp = getDataPaste(tmp)
        if tmp == "":
            continue
    tmpS = textProcess(tmp)
    Output(tmpS)
    findAnswer(tmpS)
