# encoding: utf-8

#
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from gualib import log


# 先要初始化一个 Flask 实例
app = Flask(__name__)

# message_list 用来存储所有的 message
# 因为数据都存储在内存中
# 所以重启程序数据就消失了
message_list = []

# 定义路由和路由处理函数的方式如下
# ==========================
# 用 app.route 函数定义路由，参数是一个 path 路径
# 下一行紧跟着的函数是处理这个请求的函数
# @ 是一个叫装饰器的东西, 现在无必要知道具体的原理, 只要用它就好了
# 注意 methods 参数是一个 list，它规定了这个函数能接受的 HTTP 方法
@app.route('/', methods=['GET'])
def index_view():
    """
    index_view 是路由函数，函数名随便取
    返回值会被 flask 当做 HTTP body 返回给客户端（浏览器）
    HTTP header 是 flask 自动添加的
    """
    return 'Hello Gua <br> <a href="/message">留言</a>'


# 这是访问 /message 的请求
# methods 默认是 ['GET'] 因此可以省略
@app.route('/message')
def message_view():
    # 打印请求的方法 GET 或者 POST
    log('请求方法', request.method)

    # render_template 是一个 flask 内置函数
    # 它的作业是读取并返回 templates 文件夹中的模板文件
    # messages 是传给模板的参数，这样就能在模板中使用这个变量了
    return render_template('message_index.html', messages=message_list)


# 这个路由函数只支持 POST 方法
@app.route('/message/add', methods=['POST'])
def message_add():
    """
    浏览器发送来的数据是在 HTTP body 中
    由于浏览器 form 标签提交的格式是固定的
    所以 flask 自动解析了数据
    生成一个特殊的字典存放在 request.form 中
    """
    # request.form 是 flask 保存 POST 请求的表单数据的属性
    log('request, POST 的 form 表单数据', request.form)
    # 把数据生成一个 dict 存到 message_list 中去
    msg = {
        'content': request.form.get('msg_post', ''),
    }
    message_list.append(msg)

    # 我们发送一个 302 重定向给浏览器
    # 这和我们写过的函数是一样的
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
