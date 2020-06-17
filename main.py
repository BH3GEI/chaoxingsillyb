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
import MessageSender

__header = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Authorization': ""
}

__token = "3d0da4a49407f37445a667768ff8f4ab"
__questionList = []
searched = 1
tasks = 0


def save(dicto):
    __questionList.append(dicto)


def push(message):
    # MessageBox(0, message, "答案", MB_OK)
    ptDict = {'title': "第"+message['no']+"题、"+message['question'], 'content': message['answer']}
    m = MessageSender.MessageSender("Bark")
    m.config({'apikey': "gpKSL4RQYEZyTiKyz9vtEe"})
    len = int(ptDict['content'].__len__())
    m.send(ptDict)
    if len <= 10:
        #time.sleep(0)
        pass
    elif len <= 20:
        time.sleep(3)
    else:
        time.sleep(5)



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
    b.get("https://www.baidu.com/s?wd=" + parse.quote(question))
    # b.find_element_by_id("kw").send_keys(question)
    # b.find_element_by_id("su").click()


def findAnswer(a, times):
    if times == 4:
        raise Exceptions.NoAnswerFound
    courseid = "206267220"
    g = getter.getter()
    str = ""
    j = ['I', 'II', 'III', 'IV']
    h = 0
    try:
        tmp = g.get({'q': a['question'], 'curs': courseid, 'type': a['type'], 'token': __token})
    except Exceptions.NoAnswerFound:
        try:
            r = findAnswer(a, times+1)
        except:
            getFromBaidu(a['question'])
        else:
            return r
    except ConnectionError:
        return "连接出错"
    else:
        for i in tmp:
            if i['answer'] == "":
                continue
            str += j[h] + ". : " + i['answer']
            str += "\1"
            h += 1
        save({'no': a['no'], 'question': a['question'], 'answer': str})


def threadSearch(cf, st, en):
    loop = 1
    global searched, tasks
    for i in cf.sections():
        if loop < st:
            loop += 1
            continue
        if loop >= en:
            break
        print("查找中...第%d/%d题 : " % (searched, tasks) + cf.get(i, "question"))
        searched += 1
        findAnswer({'no': i, 'question': cf.get(i, "question"), "type": cf.get(i, "type")},0)
        cf.remove_section(i)
        loop += 1


def textProcess(text, times):
    targetText = text
    if times == 0:
        targetText = targetText.strip()
        targetText = targetText.replace(" ", '')
        targetText = targetText.replace("\n", '')
        targetText = targetText.replace("\t", '')
        targetText = targetText.replace("\r", '')
        targetText = targetText.replace("\xa0", '')
        targetText = targetText.replace("\x20", '')
        targetText = targetText.replace("\u3000", '')
        targetText = targetText.replace("1、", " ")
        targetText = targetText.replace("2、", " ")
        targetText = targetText.replace("3、", " ")
        targetText = targetText.lstrip()
        targetText = targetText.rstrip()
    elif times == 1:
        targetText = targetText.replace("（", ")")
        targetText = targetText.replace("）", ")")
        targetText = targetText.replace("，", ",")
        targetText = targetText.replace("。", " ")
    elif times == 2:
        targetText = targetText.replace("(", "（")
        targetText = targetText.replace(")", "）")
        targetText = targetText.replace(",", "，")
    else:
        pattern = r'，|,|。|;|：|:|;'
        str1, str2, str3, str4, str5 = re.split(pattern, targetText)
        targetText = str1
    return targetText


def startSearch():
    # 初始化题目文件
    global __questionList,tasks
    cfg = configparser.ConfigParser()
    cfg.read("questions.ini", encoding="utf-8")
    threadNum = 6
    searched = 1
    tasks = int(cfg.sections().__len__())

    t = []
    for i in range(0, threadNum):
        maxRange = tasks * (i + 1) / threadNum + 1
        minRange = tasks * i / threadNum + 1
        t.append(threading.Thread(target=threadSearch, args=(cfg, minRange, maxRange)))
        t[i].start()

    for i in t:
        i.join()

    with open("questions.ini", "w+") as f:
        cfg.write(f)
        f.close()
    del cfg
    cfg = configparser.ConfigParser()
    for i in __questionList:
        cfg.add_section(i['no'])
        cfg.set(i['no'], "question", i['question'])
        cfg.set(i['no'], "answer", i['answer'])

    with open("answers.ini", "w", encoding="utf-8") as f:
        cfg.write(f)
        f.close()
    del cfg

    __questionList = []


def oneToN(str):
    return str.replace("\1","\n",999)


def getAnswers():
    cfg = configparser.ConfigParser()
    cfg.read("answers.ini", encoding="utf-8")
    for i in range(1,int(cfg.sections().__len__())+1):
        __questionList.append({'no':str(i),'question': cfg.get(str(i),"question"),'answer':oneToN(cfg.get(str(i),"answer"))})


last_string = pyperclip.paste()
APP_ID = '19124804'
API_KEY = 'cCMaB793Gff1w6yE9HojaE4z'
SECRET_KEY = 'PMMOEcom53RHgXpwXfoHObilbf4V3oQe'
# 初始化AipOcr
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
tmp = ""
baiduAPI = True

startSearch()
getAnswers()
for i in __questionList:
    push(i)
quit()
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
    startSearch()
