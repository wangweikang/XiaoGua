'''
POST /add?id=1 HTTP/1.1
Host: localhost:3000
Connection: keep-alive
Content-Length: 8
Cache-Control: max-age=0
Origin: http://localhost:3000
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: http://localhost:3000/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8

task=gua
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
HTTP header 大全
host 表示服务器的主机和端口，没有端口说明是默认端口 80
Content-Length body的长度
cache-control 。。。。
Origin 。。。。。
User-Agent 浏览器自己的标识字符串
Content-Type body里面的数据的类型，常见类型如下
    text/html html文件
    application/x-www-form-urlencoded 浏览器的表单格式
        a=b&c=d&e=%201
Accept 浏览器接受的数据类型   
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
r.method = 'POST'
r.path = '/add'
r.query = {
    'id': '1'
}
r.headers = {}
r.body = 'task=gua'
r.form = {
    'task': 'gua'
}