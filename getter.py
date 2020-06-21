import requests
from urllib import parse
import json
import Exceptions
import threading

class getter:
    __list = ["API4", "API1"]
    __result = []
    def get(self, arg):
        self.__result = []
        j = 0
        t = []
        noAnswerError = 0
        for i in self.__list:
            try:
                self.__result.append(eval("self." + i)(arg))
                #t.append(threading.Thread(target=getattr(self,i),args=(arg)))
                #t[j].start()
            except:
                noAnswerError += 1
                continue
            if self.__result[j]['status'] is False:
                noAnswerError += 1
            j += 1
        if noAnswerError == j:
            raise Exceptions.NoAnswerFound
        return self.__result

    def oneToSharp(self,str):
        return str.replace("\1","#",999)

    def API1(self, a):
        url = "http://qs.nnarea.cn/chaoxing_war/topicServlet?action=query&q="
        r = {'answer':"",'status':False}
        tmp = json.loads(requests.post(url + parse.quote(a['q']), '&course=' + parse.quote(str(a['curs'])) + '&type=' + str(a['type'])).text)
        if tmp['data'] != "目前没思路，等3min左右刷新页面试试":
            r['status'] = True
            r['answer'] += self.oneToSharp(tmp['data'])
        # type类型已知，无需循环4遍
        return r

    def API2(self, a):
        url = "http://cx.icodef.com/wyn-nb"
        r = {'answer':"",'status':False}
        for i in range(0, 4):
            tmp = requests.post(url, "question=" + parse.quote(a['q']) + '&type=' + str(i)).text
            if tmp != "题目不能为nil":
                r['status'] = True
                r['answer'] += tmp + "|"
        return r

    def API4(self, a):
        url = "https://api3.4n0a.cn/jsapi.php?"
        tmp = json.loads(requests.get(url + "q=" + parse.quote(a['q']) + "&token=" + a['token']).text)
        r = {'answer':"",'status':False}
        if tmp['msg'] != "可能过几天就有这道题了":
            r['status'] = True
            r['answer'] = self.oneToSharp(tmp['da'])
        return r
