# chaoxingsillyb
满分的故事

# 声明
本项目仅学习交流使用，切勿将其用于违法犯罪！请于下载后24小时内删除！本人不对该项目造成的任何后果负责

# 程序逻辑
- 自动截屏或用户手动复制所有题目，创建`questions.ini`，其内容为：  

        [题号]
        question = 问题内容
        type = 问题类型（单选题0，多选题1，填空题2，判断题3）
        
- 读取`question.ini`，并且根据`threadNum`创建对应数量线程搜索题目，以字典形式保存在全局变量`__questionList`中，在全部搜索完之后保存到`answers.ini`中，格式同上。并且，每道题如果搜索不到，还会尝试变化形式重新搜索（总共4次），搜索不到会打开百度；如果搜索到，则将此题从`questions.ini`中移除。
- 搜索完成后，使用`push(message)`方法推送给用户，使用`MessageSender`中的方法，有Bark、ServerChan、SMTP、控制台、文件等方法。其中，`message`为字典，格式为：`{'no': 题号, 'question': 题目题干, 'answer': 题目答案}`（可直接使用`__questionList`或`answers.ini`中的字典）
- 需要注意，在`__questionList`或`answers.ini`中，`\n`作为`\1`保存，使用时需替换。

# 题目获取
- 安卓端与电脑adb连接后使用universal copy复制后可直接同步到电脑剪切板
- ios端投屏在电脑截图后使用腾讯ocr获取题目文本

# 备注
- 如果要加入忽略用户截图顺序的功能，首先要改变`__questionList`的排序方式，变为1,11,12这样的排序（把`int()`去掉即可)
- 其次在检测问题类型的时候，检测一下前面的大题题号（可选）。  
当时的代码如下：
  ```python
  if lastType != detectQuestionType(textProcess(tmp,0)):
    tp += nowNum
  ```

# 待办事项
- [X] 关键字优化（连接错误以及无答案时按照标点截短后文字重搜、第一次先保留括号如果四个均无答案则去掉括号重搜）
- [X] 显示优化（四个均无答案则自动弹出百度搜索结果、每次搜索前显示所搜索的关键字）
- [X] 引擎优化（多线程
- [X] 数据库引入：没有查到的题录入待查数据库，稍后利用其它线程重新查询
- [X] 可以考虑先浏览一遍所有题，分别截图保存到不同文件中，再开双线程进行OCR和查题，最后按照题号输出，这样会快很多
- [X] 运行前提示用户选择，手动搜题模式实时显示答案，不需要进行文本处理。
- [ ] 加入一个类似搜索引擎的玩意，直接从教材里搜东西
- [ ] 自动切换OCR与剪切板复制功能，如果用户10秒没得输入，就自动保存题库，然后开始搜题，之后切换到手动模式。
- [ ] 对半砍题干可以提高搜索成功率
- [ ] 寻求更多可靠的题库api
- [ ] 蜜汁报错？？？
-
- 新增几个api（我比较菜，找不明白）：
- 【这十几个api咱们总不能等挨个查完再出答案，能不能设置个多线程，同时访问，有结果出来了就直接弹出，剩下的慢慢查，以后放到ini文件里面】
- 【有的直接输入题目就能出答案，有的不行但是脚本能用，你可以找一下这个url的位置然后康康上下文是不是有加密。我看不出来，太菜了。】
- 【有些无token，仅有url；有些不全，搜题报错比较多；有的似乎已经挂了，也可能是设置了加密；有些写的有token，但是我找不到】
- 
- I
- http://lyck6.cn/token/api2.php  http://lyck6.cn/token/newapi.php    http://cx.lyck6.cn/api/newapi1.php
- 来自网址https://greasyfork.org/zh-CN/scripts/401715-%E8%B6%85%E6%98%9F%E5%B0%94%E9%9B%85%E5%AD%A6%E4%B9%A0%E9%80%9A%E8%80%83%E8%AF%95%E4%B8%93%E7%89%88-%E4%B8%AA%E4%BA%BA%E9%A2%98%E5%BA%93-%E6%9C%80%E6%96%B0%E7%89%88%E5%8F%AF%E7%AD%94%E9%A2%98/code
- 找不到token
-
- II
- 来自网址https://greasyfork.org/zh-CN/scripts/401447-%E8%B6%85%E6%98%9F%E7%BD%91%E8%AF%BE%E5%8A%A9%E6%89%8B-%E6%94%B9-%E6%9F%A5%E9%A2%98%E5%8F%AF%E7%94%A8/code
- api和token都找不到，url似乎被拆开了
-
- III
- http://jiaoben.s759n.cn/chati.php?w=
- 来自网址https://greasyfork.org/zh-CN/scripts/403311-%E8%B6%85%E6%98%9F%E5%AD%A6%E4%B9%A0%E9%80%9A%E7%BD%91%E8%AF%BE%E5%8A%A9%E6%89%8B-%E6%9C%80%E7%89%9B%E9%A2%98%E5%BA%93-%E6%94%AF%E6%8C%81%E9%83%A8%E5%88%86%E4%B8%93%E4%B8%9A%E8%AF%BE/code
-
- IV
- https://wk.92e.win/wkapi.php?q=
- 来自网址https://greasyfork.org/zh-CN/scripts/401968-%E8%B6%85%E6%98%9F%E5%B0%94%E9%9B%85%E5%AD%A6%E4%B9%A0%E9%80%9A-%E8%80%83%E8%AF%95%E7%89%88-%E4%BF%AE%E5%A4%8D%E7%89%88-%E9%A2%98%E5%BA%93%E5%8F%AF%E7%94%A8/code
-
- V
- http://ql.hackusb.cn/yourbin_sql.php?tm=
- 来自网址https://greasyfork.org/zh-CN/scripts/402147-%E8%B6%85%E6%98%9F%E5%B0%94%E9%9B%85%E5%AD%A6%E4%B9%A0%E9%80%9A%E8%80%83%E8%AF%95-%E8%80%83%E8%AF%95%E4%B8%93%E7%89%88-%E6%9C%80%E6%96%B0%E5%8F%AF%E7%94%A8/code
-
- VI
- http://jb.s759n.cn/chati.php?w=
- 来自网址https://greasyfork.org/zh-CN/scripts/403587-%E8%B6%85%E6%98%9F%E7%BD%91%E8%AF%BE%E5%8A%A9%E6%89%8B-%E6%9C%80%E6%96%B0%E8%80%83%E8%AF%95%E4%B8%93%E7%89%88%E5%8F%AF%E7%AD%94%E9%A2%98/code
-
- VII
- http://api.xmlm8.com/tp/tk.php?t=
- 来自网址https://greasyfork.org/zh-CN/scripts/401685-%E7%86%8A%E7%8C%AB%E8%B6%85%E6%98%9F%E7%BD%91%E8%AF%BE%E5%8A%A9%E6%89%8B-%E8%80%83%E8%AF%95%E7%89%88/code
-
- VIII
- http://p.52dw.net:81/chati?q=
- 来自网址https://greasyfork.org/zh-CN/scripts/404249-%E8%B6%85%E6%98%9F%E4%BD%9C%E4%B8%9A-%E8%80%83%E8%AF%95%E8%87%AA%E5%8A%A8%E7%AD%94%E9%A2%98%E8%84%9A%E6%9C%AC-%E4%BD%9C%E8%80%85-skeleton/code
-
- IX
- http://imnu.52king.cn/api/wk/index.php?c=
- 来自网址https://greasyfork.org/zh-CN/scripts/401478-%E8%B6%85%E6%98%9F%E7%BD%91%E8%AF%BE%E5%8A%A9%E6%89%8B-%E9%A2%98%E5%BA%93%E4%BF%AE%E5%A4%8D%E7%89%88/code
- 
- X
- http://panel.52wfy.cn/browserapi.php?op=get&bid=
- 来自网址https://greasyfork.org/zh-CN/scripts/390924-%E8%B6%85%E6%98%9F-%E6%99%BA%E6%85%A7%E6%A0%91%E6%89%B9%E9%87%8F%E5%88%B7%E8%AF%BE%E5%8A%A9%E6%89%8B-%E8%87%AA%E5%8A%A8%E7%99%BB%E5%BD%95%E8%B4%A6%E5%8F%B7-%E8%87%AA%E5%8A%A8%E8%BF%9B%E5%85%A5%E8%AF%BE%E7%A8%8B/code
-
- XI
- http://129.204.175.209/cha_xin.php
- 来自网址https://greasyfork.org/zh-CN/scripts/401563-%E8%B6%85%E6%98%9F%E7%BD%91%E8%AF%BE%E5%8A%A9%E6%89%8B-%E6%94%B9-%E6%9F%A5%E9%A2%98%E5%8F%AF%E7%94%A8-%E8%87%AA%E5%8A%A8%E7%AD%BE%E5%88%B0%E5%8F%AF%E7%94%A8/code
- 这个似乎有加密？
- 
- XII
- http://106.52.197.16:8080/chaoxing_war/topicServlet?action=query&q=
- 来自网址https://greasyfork.org/zh-CN/scripts/403911-%E8%B6%85%E6%98%9F%E5%B0%94%E9%9B%85%E5%AD%A6%E4%B9%A0%E9%80%9A%E7%BD%91%E8%AF%BE%E5%8A%A9%E6%89%8B-%E6%9C%80%E5%BC%BA%E9%A2%98%E5%BA%93-%E7%B2%BE%E5%87%86%E7%AD%94%E9%A2%98/code

