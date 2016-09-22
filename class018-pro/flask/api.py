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
    return w.json()


@main.route('/comment', methods=['POST'])
def comment():
    form = request.form
    u = current_user()
    c = Comment(form)
    c.name = u.username
    if c.valid():
        c.save()
    return redirect(url_for('.index'))
