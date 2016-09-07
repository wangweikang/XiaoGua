# encoding: utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

import time


# 先要初始化一个 Flask 实例
app = Flask(__name__)

# message_list 用来存储所有的 message
message_list = []

# 用 log 函数把所有输出写入到文件，这样就能很方便地掌控全局了
# 即便你关掉程序，也能再次打开来查看，这就是个时光机 (
def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    # 中文 windows 平台默认打开的文件编码是 gbk 所以需要指定一下
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        # 通过 file 参数可以把输出写入到文件 f 中
        # 需要注意的是 **kwargs 必须是最后一个参数
        print(dt, *args, file=f, **kwargs)


# 定义路由和路由处理函数的方式如下
# ==========================
# 用 app.route 函数定义路由，参数是一个 path 路径
# 下一行紧跟着的函数是处理这个请求的函数
# @ 是一个叫装饰器的东西, 现在无必要知道具体的原理, 只要用它就好了
# 注意 methods 参数是一个 list，它规定了这个函数能接受的 HTTP 方法
@app.route('/', methods=['GET'])
def hello_world():
    """
    路由函数 return 的是 body
    """
    return 'Hello Gua'


# 这是访问 /message 的请求
# methods 默认是 ['GET'] 因此可以省略
@app.route('/message')
def message_view():
    # 打印请求的方法 GET 或者 POST
    log('msg view 请求方法', request.method)

    # request.args 是 flask 保存 URL 中的参数的属性
    # 访问 http://127.0.0.1:2000/message?a=1
    # 会打印如下输出 (ImmutableMultiDict 是 flask 的自定义类型, 意思是不可以改变的字典)
    # request ImmutableMultiDict([('a', '1')])
    log('request, query 参数', request.args)

    # render_template 是一个 flask 内置函数
    # 它的作用是读取并返回 templates 文件夹中的模板文件
    # messages 是传给模板的参数，这样就能在模板中使用这个变量了
    return render_template('message_index.html',
                           messages=message_list)


# 这个路由函数只支持 POST 方法
@app.route('/message/add', methods=['POST'])
def message_add():
    # 打印请求的方法 GET 或者 POST
    log('message_add 请求方法', request.method)

    # request.form 是 flask 保存 POST 请求的表单数据的属性
    log('request, POST 的 form 表单数据', request.form)
    # 把数据生成一个 dict 存到 message_list 中去
    msg = {
        'content': request.form.get('msg_post', ''),
    }
    message_list.append(msg)

    # 这和我们写过的函数是一样的
    # return redirect('/message')
    # 一般来说，我们会用 url_for 生成路由，如下
    # 注意, url_for 参数是路由函数的名字（格式为字符串）
    return redirect(url_for('message_view'))


# 运行服务器
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
    # app.run() 开始运行服务器
    # 所以你访问下面的网址就可以打开网站了
    # http://127.0.0.1:2000/
