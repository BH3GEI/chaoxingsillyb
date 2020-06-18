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


def detectQuestionType(question):
    if "单选题" in question:
        type = 0
    elif "多选题" in question:
        type = 1
    elif "判断题" in question:
        type = 2
    else:
        type = 3
    return type


def detectQuestionNum(question):
    p1, p2 = question.split('/', 2)  # 按照分数线/分隔，因为全屏仅此一个
    numOrig = p2[0:5]  # 取第二段的前五个字符
    listOrig = re.findall("(\d+)", numOrig)  # 挑出数字
    numMidd = listOrig[0]
    # 合并list，以防ocr空格分开数字
    num = int(numMidd)
    return num


def detectQuestionID(question):
    listOrig = re.findall("(\d+)", question)  # 挑出数字
    numMidd = listOrig[0]
    # 合并list，以防ocr空格分开数字
    num = int(numMidd)
    return num


def preProcessQuestion(question):
    m1 = question.split('A', 2)  # 以A为分割
    question = m1[0]  # 取前一半
    n1 = list(question.split("分)", 2))
    n1.pop(0)
    return n1[0]


def detectQuestion(question):
    n1 = preProcessQuestion(question)
    print(n1)
    question = ""
    for i in n1:
        question += i
    if re.findall("(\d+)、",question):
        question = question.replace("、","",1)
    question = question[1:]
    return question


def push(message):
    # MessageBox(0, message, "答案", MB_OK)
    ptDict = {'title': "第" + message['id'] + "题、" + message['question'], 'content': message['answer']}
    m = MessageSender.MessageSender("Bark")
    m.config({'apikey': "gpKSL4RQYEZyTiKyz9vtEe"})
    len = int(ptDict['content'].__len__())
    m.send(ptDict)
    if len <= 10:
        # time.sleep(0)
        pass
    elif len <= 20:
        time.sleep(3)
    else:
        time.sleep(5)


def getDataOCR(aipOcr, times):
    if times >= 4:
        raise ConnectionError
    img1 = ImageGrab.grabclipboard()
    if img1 is None:
        raise Exceptions.ClipNotIMG("剪切板不是图片")
    # print(type(img))
    # 文件保存的名字
    img_path = 'question.png'
    # 保存图片
    img1.save(img_path)
    # 百度api执行所需数据，运行需换成自己的APP_ID，API_KEY，SECRET_KEY

    with open(img_path, 'rb') as f:
        img2 = f.read()
        f.close()
    # print(type(img2))
    # 识别图片并返回结果
    try:
        result = aipOcr.basicGeneral(img2)
    except ConnectionError:
        print("asss")
        return "ConnectionError"
    except:
        print("???")
        data = getDataOCR(aipOcr, times + 1)

    data = ''
    for r in result['words_result']:
        data = data + r['words']
    time.sleep(1)
    return data


def getDataPaste(last):
    tmp = pyperclip.paste()
    if tmp == last:
        return ""
    return tmp


def getFromBaidu(question):
    print("shit!")


def findAnswer(a, times):
    if times == 4:
        raise Exceptions.NoAnswerFoundAtAll
    courseid = "206267220"
    g = getter.getter()
    str = ""
    j = ['I', 'II', 'III', 'IV']
    h = 0
    try:
        tmp = g.get({'q': a['question'], 'curs': courseid, 'type': a['type'], 'token': __token})
    except Exceptions.NoAnswerFound:
        try:
            r = findAnswer(textProcess(a,times+1), times + 1)
        except Exceptions.NoAnswerFoundAtAll:
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
        return {'id': a['id'], 'question': a['question'], 'answer': str}


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
        save(findAnswer({'id': i, 'question': cf.get(i, "question"), "type": cf.get(i, "type")}, 0))
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
        targetText = targetText.lstrip()
        targetText = targetText.rstrip()
    elif times == 1:
        targetText = targetText.replace("（", ")")
        targetText = targetText.replace("）", ")")
        targetText = targetText.replace("，", ",")
        targetText = targetText.replace("。", " ")
        targetText = targetText.replace("(", "（")
        targetText = targetText.replace(")", "）")
        targetText = targetText.replace(",", "，")
    elif times == 2:
        targetText = targetText[0:int(targetText.__len__())/2]
    else:
        pattern = r'，|,|。|;|：|:|;'
        str1= re.split(pattern, targetText)
        targetText = str1[0]
    return targetText


def sortByEleID(element):
    return element['id']


def startSearch():
    # 初始化题目文件
    global __questionList, tasks
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
    __questionList.sort(key=sortByEleID)
    cfg = configparser.ConfigParser()
    for i in __questionList:
        cfg.add_section(i['id'])
        cfg.set(i['id'], "relativeID", i['rID'])
        cfg.set(i['id'], "question", i['question'])
        cfg.set(i['id'], "answer", i['answer'])

    with open("answers.ini", "w", encoding="utf-8") as f:
        cfg.write(f)
        f.close()
    del cfg


def oneToN(str):
    return str.replace("\1", "\n", 999)


def nToOne(str):
    return str.replace("\n", "\1", 999)


lastString = ""
appID = '18825234'#'19124804'
apiKey = 'eRwWUDBfne3iKuRD1csC25Ga'#'cCMaB793Gff1w6yE9HojaE4z'
secretKey = 'e6nF9IZ7fGpt0EudikQYeUZID2DFf6GN'#'PMMOEcom53RHgXpwXfoHObilbf4V3oQe'
# 初始化AipOcr
aipOcr = AipOcr(appID, apiKey, secretKey)
tmp = ""
baiduAPI = True

cfg = configparser.ConfigParser()

initFlag = True
numOfQuestions = 0
nowNum = 0
tp = 0
lastType = 0

# 手动模式
manualMode = True
startTime = time.time()
if manualMode:
    while 101 != nowNum:
        if baiduAPI:
            try:
                tmp = getDataOCR(aipOcr, 0)
            except Exceptions.ClipNotIMG:
                tmp = getDataPaste("")
            except:
                continue
        else:
            tmp = getDataPaste(tmp)
            if tmp == "":
                continue
        if lastString == textProcess(tmp, 0):
            endTime = time.time()
            if endTime - startTime >= 3000:
                quit()
            continue
        else:
            startTime = time.time()
            lastString = textProcess(tmp,0)
            nowNum+=1
            print(findAnswer({'id': 0,'question': textProcess(tmp,0), 'type':0},0)['answer'])

quit()
print("开始初始化...")
while initFlag:
    try:
        numOfQuestions = detectQuestionNum(getDataOCR(aipOcr, 0))
    except:
        continue
    else:
        initFlag = False

print("开始获取题目内容...")
while (nowNum - numOfQuestions) != 0:
    if baiduAPI:
        try:
            tmp = getDataOCR(aipOcr, 0)
        except Exceptions.ClipNotIMG:
            tmp = getDataPaste("")
        except:
            continue
    else:
        tmp = getDataPaste(tmp)
        if tmp == "":
            continue
    if lastString == detectQuestion(textProcess(tmp, 0)):
        continue
    if lastType != int(detectQuestionType(textProcess(tmp, 0))):
        tp = nowNum

    q = textProcess(tmp, 0)
    nowNum += 1
    try:
        lastString = detectQuestion(q)
        lastType = int(detectQuestionType(q))
        print("第%d/%d题:" %(nowNum, numOfQuestions) + detectQuestion(q))
        #now = nowNum
        now = detectQuestionID(preProcessQuestion(q)) + tp
        cfg.add_section(str(lastType)+str(now))
        cfg.set(str(lastType)+str(now), "relativeID", str(now))
        cfg.set(str(lastType)+str(now), "question", detectQuestion(q))
        cfg.set(str(lastType)+str(now), "type", str(detectQuestionType(q)))
    except:
        nowNum -= 1
        continue

with open("questions.ini", "w", encoding="utf-8") as f:
    cfg.write(f)
    f.close()
    del cfg

print("开始查找...")
startSearch()
print("正在推送...")
for i in __questionList:
    print("第%d/%d题..." % (int(i['ID']),numOfQuestions))
    push(i)
