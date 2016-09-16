from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort
from flask import session

from models import User
from models import Weibo
from models import Comment


# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('weibo', __name__)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


@main.route('/<username>/timeline')
def timeline_view(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    else:
        # ws = Weibo.query.filter_by(user_id=u.id).all()
        ws = u.weibos()
        for w in ws:
            w.load_comments()
        return render_template('timeline.html', weibos=ws)


@main.route('/weibo/add', methods=['POST'])
def add():
    u = current_user()
    if u is not None:
        print('weibo add', u.id, u.username, u.password)
        form = request.form
        w = Weibo(form)
        w.user_id = u.id
        w.save()
        return redirect(url_for('.timeline_view', username=u.username))
    else:
        abort(401)


@main.route('/comment/add', methods=['POST'])
def comment_add():
    u = current_user()
    if u is not None:
        print('comment_add', u.id, u.username)
        form = request.form
        c = Comment(form)
        c.user_id = u.id
        c.weibo_id = int(form.get('weibo_id', -1))
        c.save()
        return redirect(url_for('.timeline_view', username=u.username))
    else:
        abort(401)

