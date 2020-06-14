import pyperclip
import requests
import json
from urllib import parse
import getter
from win32api import MessageBox
from win32con import MB_OK
import time

__header = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Authorization': ""
}

__token = ""


def Output(message):
    # MessageBox(0, message, "答案", MB_OK)
    print(message)


# clip = pyperclip.paste()


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


last_string = pyperclip.paste()
while True:
    time.sleep(0.1)
    string = pyperclip.paste()
    if string != last_string and string != '':
        last_string = string
        findAnswer(last_string)
