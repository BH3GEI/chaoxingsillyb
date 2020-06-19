import requests
import hmac
import hashlib
import base64
import time
import random
import re
from aip import AipOcr


class OcrApis:
    __list = [ "tencent"]

    def get(self, arg):
        result = []
        j = 0
        connectionError = 0
        for i in self.__list:
            try:
                result.append(eval("self." + i)(arg))
            except:
                connectionError += 1
                continue
            j += 1
            time.sleep(1)
        if connectionError == j:
            raise ConnectionError
        return result

    def oneToSharp(self, str):
        return str.replace("\1", "#", 999)

    def tencent(self, a):
        appid = a['tencentAppID']
        # bucket = " 这个是优图上面的，可以不填"  # 参考本文开头提供的链接
        secretID = a['tencentSecretID']  # 参考官方文档
        secretKey = a['tencentSecretKey']  # 同上
        expired = time.time() + 2592000
        onceExpired = 0
        current = time.time()
        rdm = ''.join(random.choice("0123456789") for i in range(10))
        userid = "0"
        fileid = "tencentyunSignTest"
        # + "&b=" + bucket
        info = "a=" + appid + "&k=" + secretID + "&e=" + str(expired) + "&t=" + str(
            current) + "&r=" + str(
            rdm) + "&u=0&f="

        signindex = hmac.new(bytes(secretKey, 'utf-8'), bytes(info, 'utf-8'), hashlib.sha1).digest()  # HMAC-SHA1加密
        sign = base64.b64encode(signindex + bytes(info, 'utf-8'))  # base64转码，也可以用下面那行转码
        # sign=base64.b64encode(signindex+info.encode('utf-8'))

        url = "http://recognition.image.myqcloud.com/ocr/general"
        headers = {'Host': 'recognition.image.myqcloud.com',
                   "Authorization": sign,
                   }
        files = {'appid': (None, appid),
                 # 'bucket': (None, bucket),
                 'image': ('question.jpg', a['file'], 'image/jpeg')
                 }

        r = requests.post(url, files=files, headers=headers)

        responseinfo = r.content
        data = responseinfo.decode('utf-8')

        r_index = r'itemstring":"(.*?)"'  # 做一个正则匹配
        result = re.findall(r_index, data)
        data = ""
        for i in result:
            data += i
        return data

    def baidu(self, a):
        aipOcr = AipOcr(a['baiduAppID'], a['baiduSecretID'], a['baiduSecretKey'])
        result = aipOcr.basicGeneral(a['file'])
        data = ''
        for r in result['words_result']:
            data = data + r['words']
        return data
