'''
网址组成（四部分）
    协议      http, https（https 是加密的 http）
    主机      g.cn  zhihu.com之类的网址
    端口      HTTP 协议默认是 80，因此一般不用填写
    路径      下面的「/」和「/question/31838184」都是路径
http://www.zhihu.com/
http://www.zhihu.com/question/31838184



电脑通信靠IP地址，IP地址记不住就发明了域名（domain name）
然后电脑自动向DNS服务器（domain name server）查询域名对应的IP地址

比如g.cn这样的网址，可以通过电脑的ping程序查出对应 IP 地址
➜    ping g.cn
PING g.cn (74.125.69.160): 56 data bytes



端口是什么？
一个比喻：
用邮局互相写信的时候，ip相当于地址（也可以看做邮编，地址是域名）
端口是收信人姓名（因为一个地址比如公司、家只有一个地址，但是却可能有很多收信人）
端口就是一个标记收信人的数字。
端口是一个 16 位的数字，所以范围是 0-65535（2**16）



——HTTP协议——

一个传输协议，协议就是双方都遵守的规范。
为什么叫超文本传输协议呢，因为收发的是文本信息。
1，浏览器（客户端）按照规定的格式发送文本数据（请求）到服务器
2，服务器解析请求，按照规定的格式返回文本数据到浏览器
3，浏览器解析得到的数据，并做相应处理

请求和返回是一样的数据格式，分为4部分：
1，请求行或者响应行
2，Header（请求的 Header 中 Host 字段是必须的，其他都是可选）
3，\r\n\r\n（连续两个换行回车符，用来分隔Header和Body）
4，Body（可选）

请求的格式，注意大小写（这是一个不包含Body的请求）：
原始数据如下
'GET / HTTP/1.1\r\nhost:g.cn\r\n\r\n'
打印出来如下
GET / HTTP/1.1
Host: g.cn

其中
1， GET 是请求方法（还有POST等，这就是个标志字符串而已）
2，/ 是请求的路径（这代表根路径）
3，HTTP/1.1  中，1.1是版本号，通用了20年

具体字符串是 'GET / HTTP/1.1\r\nhost:g.cn\r\n\r\n'


返回的数据如下
HTTP/1.1 301 Moved Permanently
Alternate-Protocol: 80:quic,p=0,80:quic,p=0
Cache-Control: private, max-age=2592000
Content-Length: 218
Content-Type: text/html; charset=UTF-8
Date: Tue, 07 Jul 2015 02:57:59 GMT
Expires: Tue, 07 Jul 2015 02:57:59 GMT
Location: http://www.google.cn/
Server: gws
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block



Body部分太长，先不贴了
其中响应行（第一行）：
1，HTTP/1.1 是版本
2，301 是「状态码」，参见文末链接
3，Moved Permanently 是状态码的描述
浏览器会自己解析Header部分，然后将Body显示成网页



——web服务器做什么——

主要就是解析请求，发送相应的数据给客户端。
例如附件中的代码（1client.py）就是模拟浏览器发送 HTTP 请求给服务器并把收到的所有信息打印出来（使用的是最底层的 socket，现阶段不必关心这种低层，web开发是上层开发）



附录：
HTTP状态码
https://zh.wikipedia.org/wiki/HTTP%E7%8A%B6%E6%80%81%E7%A0%81

'''