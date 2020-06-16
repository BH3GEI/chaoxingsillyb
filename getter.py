import requests
from urllib import parse
import json
import Exceptions


class getter:
    __list = ["API4", "API1", "API2"]

    def get(self, arg):
        result = []
        j = 0
        noAnswerError = 0
        connectionError = 0
        for i in self.__list:
            try:
                result.append(eval("self." + i)(arg))
            except:
                connectionError += 1
                continue
            if result[j]['status'] is False:
                noAnswerError += 1
            j += 1
        j += connectionError
        if noAnswerError == j:
            raise Exceptions.NoAnswerFound
        if connectionError == j:
            raise ConnectionError
        return result

    def API1(self, a):
        url = "http://qs.nnarea.xcn/chaoxing_war/topicServlet?action=query&q="
        r = {'answer':"",'status':False}
        for i in range(0, 4):
            tmp = json.loads(requests.post(url + parse.quote(a['q']), 'course=' + parse.quote(a['curs']) + '&type=' + str(i)).text)
            if tmp['data'] != "目前没思路，等3min左右刷新页面试试":
                r['status'] = True
                r['answer'] += tmp['data'] + "\n"
        return r

    def API2(self, a):
        url = "http://cx.icodef.com/wyn-nb"
        r = {'answer':"",'status':False}
        for i in range(0, 4):
            tmp = requests.post(url, "q=" + parse.quote(a['q']) + '&type=' + str(i)).text
            if tmp != "题目不能为nil":
                r['status'] = True
                r['answer'] += tmp + "\n"
        return r

    def API4(self, a):
        url = "https://api3.4n0a.cn/jsapi.php?"
        tmp = json.loads(requests.get(url + "q=" + parse.quote(a['q']) + "&token=" + a['token']).text)
        r = {'answer':"",'status':False}
        if tmp['msg'] != "可能过几天就有这道题了":
            r['status'] = True
            r['answer'] = tmp['da']
        return r
