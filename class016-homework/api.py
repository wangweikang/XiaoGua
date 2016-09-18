from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort

import json

from models import Weibo
from models import Comment

from user import current_user


# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('api', __name__)

# /api/weibo/add
@main.route('/weibo/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    t = Weibo(form)
    t.name = u.username
    r = {
        'data': []
    }
    if t.valid():
        t.save()
        r['success'] = True
        r['data'] = t.json()
    else:
        r['success'] = False
        message = t.error_message()
        r['message'] = message
    return json.dumps(r, ensure_ascii=False)


@main.route('/weibo/delete/<int:weibo_id>', methods=['GET'])
def delete(weibo_id):
    w = Weibo.query.get(weibo_id)
    w.delete()
    r = {
        'success': True,
        'data': w.json(),
    }
    return json.dumps(r, ensure_ascii=False)


# TODO
"""
2016/9/14
因为我已经强化了代码
所以作业只需要实现两个功能
1，评论
2，更新微博

实现步骤如下
1，现在 api.py 里实现 api 功能（记住返回数据的格式要和 上面的 delete add 相同）
2，在 api.js 里实现 js api 功能（调用服务器，照猫画虎）
3，给 html 页面中的相应元素绑定功能，在 weibo.js 中
4，需要注意的是页面中每个微博都要添加一个 更新微博 按钮
    点击这个按钮后要 append 一个 input 一个 button
    button 需要提前用事件委托绑定一个事件（用来调用 api.js 中的更新微博函数）
"""
