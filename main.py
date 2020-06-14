import pyperclip
import requests
import json
from urllib import parse

from PIL import ImageGrab
from aip import AipOcr
import getter
from win32api import MessageBox
from win32con import MB_OK
import time
import re


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

def findAnswer(a):
    courseid = "206267220"
    g = getter.getter()
    str = ""
    j = ['I', 'II', 'III', 'IV']
    h = 0
    for i in g.get({'q': a, 'curs': courseid, 'type': "1", 'token': __token}):
        str += j[h] + ". : " + i + "\n"
        str += '-' * 20
        str += "\n"
        h += 1
    Output(str)
    str = ""
    time.sleep(5)


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


last_string = pyperclip.paste()
APP_ID = '19124804'
API_KEY = 'cCMaB793Gff1w6yE9HojaE4z'
SECRET_KEY = 'PMMOEcom53RHgXpwXfoHObilbf4V3oQe'
# 初始化AipOcr
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
tmp = ""
baiduAPI = False
while True:
    time.sleep(1)
    if baiduAPI:
        tmp = getDataOCR(aipOcr)
    else:
        tmp = getDataPaste(tmp)
        if tmp == "":
            continue
    tmpS = textProcess(tmp)
    Output(tmpS)
    findAnswer(tmpS)
