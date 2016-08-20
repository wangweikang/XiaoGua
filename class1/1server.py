import socket

# 这是一个 web 服务器
# host 和 port 是服务器自己的主机和端口
# 1024 以下的端口都是保留端口，必须管理员权限才能使用
# 所以我们这个测试服务器用的端口是 2000
# host 是空字符串，表示接受任意（局域网或者外网）的连接
host = ''
port = 2000

# 新建 socket
# bind 绑定服务器的 host 和 port
s = socket.socket()
s.bind((host, port))

def read_from_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

# 用一个无限循环来接受请求
while True:
    # 用 listen 监听请求
    # 5 是一个叫做 backlog 的参数
    # 它表示 tcp 协议建立连接的三次握手队列的数量
    s.listen(5)
    connection, address = s.accept()

    # 用 recv 接收客户端发送的请求数据
    request = connection.recv(1024)

    # 打印出来信息
    request = request.decode('utf-8')
    if len(request) == 0:
        continue
    # print('ip and request, {}\n{}'.format(address, request))
    line = request.split('\n')[0]
    print('line', line)
    path = line.split()[1]
    print('path, ', path)
    # 用 sendall 把响应数据发送给客户端
    normal_response = b'Hello Gua!'
    doge_response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello Doge!<img src="img/doge0.gif"><img src="img/doge1.gif">'
    if path == '/doge':
        r = doge_response
    elif path == '/img/doge0.gif':
        r = read_from_file('doge0.gif')
    elif path == '/img/doge1.gif':
        r = read_from_file('doge1.gif')
    else:
        r = b'404 NOT FOUND'
    connection.sendall(r)

    # 用 close 关闭连接
    connection.close()

# http://localhost:2000/doge
