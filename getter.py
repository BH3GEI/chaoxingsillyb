import requests
from urllib import parse
import json
import Exceptions


class getter:
    __list = ["API4", "API1", "API2", "API3"]

    def get(self, arg):
        result = []
        for i in self.__list:
            result.append(eval("self." + i)(arg))
            if True: # To do List: 判断API返回无答案内容
                raise Exceptions.NoAnswerFound
        return result

    def API1(self, a):
        url = "http://qs.nnarea.cn/chaoxing_war/topicServlet?action=query&q="
        r = ""
        for i in range(0, 4):
            r += json.loads(
                requests.post(url + parse.quote(a['q']), 'course=' + parse.quote(a['curs']) + '&type=' + str(i)).text)[
                'data']
        return r

    def API2(self, a):
        url = "http://cx.icodef.com/wyn-nb"
        r = ""
        for i in range(0, 4):
            r += requests.post(url, "question=" + parse.quote(a['q']) + '&type=' + str(i)).text
        return r

    def API3(self, a):
        url = "http://cx.beaa.cn/cx.php"
        r = requests.post(url, "content=" + parse.quote(a['q'])).text
        return r

    def API4(self, a):
        url = "https://api3.4n0a.cn/jsapi.php?"
        r = json.loads(requests.get(url + "q=" + parse.quote(a['q']) + "&token=" + a['token']).text)
        return r['da']
