import requests
from urllib import parse
import json
import Exceptions


class getter:
    __list = ["API4", "API1", "API3", "API5", "xueXiaoYiAPI"]
    __result = []

    def get(self, arg):
        self.__result = []
        j = 0
        t = []
        noAnswerError = 0
        for i in self.__list:
            try:
                self.__result.append(eval("self." + i)(arg))
            except:
                noAnswerError += 1
                continue
            if self.__result[j]['status'] is False:
                noAnswerError += 1
            j += 1
        if noAnswerError == j:
            raise Exceptions.NoAnswerFound
        return self.__result

    def __oneToSharp(self, str):
        return str.replace("\1", "#", 999)

    def API1(self, a):
        url = "http://qs.nnarea.cn/chaoxing_war/topicServlet?action=query&q="
        r = {'answer': "", 'status': False}
        tmp = json.loads(requests.post(url + parse.quote(a['q']),
                                       '&course=' + parse.quote(str(a['curs'])) + '&type=' + str(a['type'])).text)
        if tmp['data'] != "目前没思路，等3min左右刷新页面试试":
            r['status'] = True
            r['answer'] += self.__oneToSharp(tmp['data'])
        # type类型已知，无需循环4遍
        return r

    def API4(self, a):
        url = "https://api3.4n0a.cn/jsapi.php?"
        tmp = json.loads(requests.get(url + "q=" + parse.quote(a['q']) + "&token=" + a['token']).text)
        r = {'answer': "", 'status': False}
        if tmp['msg'] != "可能过几天就有这道题了":
            r['status'] = True
            r['answer'] = self.__oneToSharp(tmp['da'])
        return r

    def xueXiaoYiAPI(self, a):
        url = "http://api2.4n0a.cn:81/zdtool.php?question="
        tmp = json.loads(requests.get(url + parse.quote(a['q'])).text)
        r = {'answer': "", 'status': False}
        if tmp['data'] != "没搜到":
            r['status'] = True
            r['answer'] = self.__oneToSharp(tmp['data'])
        return r

    def API3(self, a):
        url = "https://c.lewq.cn/ct/xxy/?n=2&tm="
        tmp = json.loads(requests.get(url + parse.quote(a['q'])).text)[0]
        r = {'answer': "", 'status': False}
        if tmp['q'] != "找不到结果，很可能是你输入的内容与题目不一致，请只输入题干部分，不能有多余的字、题目选项和错别字！！！如未收录请过几天再尝试，题目每天更新！":
            r['status'] = True
            r['answer'] = self.__oneToSharp(tmp['a'])
        return r

    def API5(self, a):
        url = "http://47.112.247.80/wkapi.php?q="
        tmp = json.loads(requests.get(url + parse.quote(a['q'])).text)
        r = {'answer': "", 'status': False}
        if tmp['answer'] != "暂未查询到答案！":
            r['status'] = True
            r['answer'] = self.__oneToSharp(tmp['answer'])
        return r
