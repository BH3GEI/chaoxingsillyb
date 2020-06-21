import pyperclip
import Exceptions
from PIL import ImageGrab
import getter
import time
import re
import configparser
import threading
import MessageSender
from OcrApis import OcrApis
from functools import cmp_to_key

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
#提取题型


def detectQuestionNum(question):
    p1, p2 = question.split('/', 2)  # 按照分数线/分隔，因为全屏仅此一个
    numOrig = p2[0:5]  # 取第二段的前五个字符
    listOrig = re.findall("(\d+)", numOrig)  # 挑出数字
    numMidd = listOrig[0]
    # 合并list，以防ocr空格分开数字
    num = int(numMidd)
    return num
#提取总题数


def detectQuestionID(question):
    listOrig = re.findall("(\d+)、", question)  # 挑出数字
    numMidd = listOrig[0]
    # 合并list，以防ocr空格分开数字
    num = int(numMidd)
    return num
#提取题号


def preProcessQuestion(question):
    m1 = question.split('A', 2)  # 以A为分割
    question = m1[0]  # 取前一半
    splitChar = "分)"
    if "分）" in question:
        splitChar = "分）"
    n1 = list(question.split(splitChar, 2))
    n1.pop(0)
    return n1[0]
#预提取题干（带题号）


def removeQuestionNum(question):
    if re.findall("(\d+)、",question):
        question = question.replace("、","",1)
        question = question.replace(str(re.findall("(\d+)", question)[0]),"",1)
    else: question = question.replace(str(re.findall("(\d+)", question)[0]),"",1)
    return question
#删除题干的题号


def detectQuestion(question):
    n1 = preProcessQuestion(question)
    question = ""
    for i in n1:
        question += i
    question = removeQuestionNum(question)
    return question
#调用上一个函数删除题号，得到纯文本题干


def halfCut(question):
    firstpart = question[:len(question) / 2], question[len(question) / 2:]
    return question
#砍两半


def commaCut(question):
    if "," in question:
        piece = question.split(',', 2)
    elif "，" in question:
        piece = question.split('，', 2)
    return piece[0]
#按逗号砍，砍成两段，两个字符串，建议都搜一遍


def push(message):
    # MessageBox(0, message, "答案", MB_OK)
    ptDict = {'title': "第" + message['section'] + "题、" + message['question'], 'content': message['answer']}
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
#推送到ios设备


def getDataOCR(times):
    g = OcrApis()
    if times >= 4:
        raise ConnectionError
    img1 = ImageGrab.grabclipboard()
    if img1 is None:
        raise Exceptions.ClipNotIMG("剪切板不是图片")
    # print(type(img))
    img_path = 'question.png'
    img1.save(img_path)
    #保存图片
    with open(img_path, 'rb') as f:
        img2 = f.read()
        f.close()
    # print(type(img2))
    # 识别图片并返回结果
    try:
        #appID = '18825234'  # '19124804'
        #apiKey = 'eRwWUDBfne3iKuRD1csC25Ga'  # 'cCMaB793Gff1w6yE9HojaE4z'
        #secretKey = 'e6nF9IZ7fGpt0EudikQYeUZID2DFf6GN'  # 'PMMOEcom53RHgXpwXfoHObilbf4V3oQe'
        result = g.get({'tencentAppID': "1302464488",
                        'tencentSecretID': "AKIDd1Rc6KFxOZT7X1wD1aNvDF5ex0nPZThg",
                        'tencentSecretKey': "rRknxrVs3zjFqDKCn9dsrZ092edOt751",
                        'baiduAppID': "19124804",
                        'baiduSecretID': "cCMaB793Gff1w6yE9HojaE4z",
                        'baiduSecretKey': "PMMOEcom53RHgXpwXfoHObilbf4V3oQe",
                        'file': img2})
    except ConnectionError:
        return "ConnectionError"
    except:
        result = getDataOCR(times + 1)
    return result[0]


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
        print("第%d遍搜索失败！" % (times+1))
        try:
            r = findAnswer(textProcess(a['question'],times+1), times + 1)
        except Exceptions.NoAnswerFoundAtAll:
            getFromBaidu(a['question'])
        else:
            return r
    else:
        print("搜索成功！")
        for i in tmp:
            if i['answer'] == "":
                continue
            str += j[h] + ". : " + i['answer']
            str += "\1"
            h += 1
        return {'section': a['section'],'id': a['id'], 'question': a['question'], 'answer': str, 'relativeID': a['relativeID']}


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
        save(findAnswer({'section': i, 'id': cf.get(i, "id"),'question': cf.get(i, "question"), "type": cf.get(i, "type"), 'relativeID': cf.get(i, "relativeID")}, 0))
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


def sortByEleID(a, b):
    a1, a2 = a['section'].split("-",2)
    b1, b2 = b['section'].split("-",2)
    a1 = int(a1)
    b1 = int(b1)
    a2 = int(a2)
    b2 = int(b2)
    if a1>b1:
        return 1
    elif a1<b1:
        return -1
    if a2>b2:
        return 1
    else:
        return -1



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
    __questionList.sort(key=cmp_to_key(sortByEleID))
    cfg = configparser.ConfigParser()
    for i in __questionList:
        cfg.add_section(i['section'])
        cfg.set(i['section'], "ID", i['id'])
        cfg.set(i['section'], "relativeID", i['relativeID'])
        cfg.set(i['section'], "question", i['question'])
        cfg.set(i['section'], "answer", i['answer'])

    with open("answers.ini", "w", encoding="utf-8") as f:
        cfg.write(f)
        f.close()
    del cfg


def oneToN(str):
    return str.replace("\1", "\n", 999)


def nToOne(str):
    return str.replace("\n", "\1", 999)


lastString = ""

# 初始化AipOcr

tmp = ""
baiduAPI = True

cfg = configparser.ConfigParser()

initFlag = True
numOfQuestions = 0
nowNum = 0
tp = 0
lastType = 0

manualMode=True
modeChoice=input("是否选择手动模式？y/n\n")


def yourMode(modeChoice):
    if modeChoice=="y":
        manualMode = True
    if modeChoice=="n":
        manualMode = False
    return manualMode


startTime = time.time()
if yourMode(modeChoice):
    while 101 >= nowNum:
        if baiduAPI:
            try:
                tmp = getDataOCR(0)
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

print("开始初始化...")
while initFlag:
    try:
        numOfQuestions = detectQuestionNum(getDataOCR(0))
    except:
        continue
    else:
        initFlag = False

print("开始获取题目内容...")
while (nowNum - numOfQuestions) != 0:
    if baiduAPI:
        try:
            tmp = getDataOCR(0)
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
        rID = detectQuestionID(preProcessQuestion(q))
        now = rID + tp
        cfg.add_section(str(lastType+1)+"-"+str(rID))
        cfg.set(str(lastType+1)+"-"+str(rID), "ID", str(now))
        cfg.set(str(lastType+1)+"-"+str(rID), "relativeID", str(rID))
        cfg.set(str(lastType+1)+"-"+str(rID), "question", detectQuestion(q))
        cfg.set(str(lastType+1)+"-"+str(rID), "type", str(detectQuestionType(q)))
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
j = 1
for i in __questionList:
    print("第%s题(%d/%d)..." % (i['section'],j,numOfQuestions))
    j=j+1
    push(i)
