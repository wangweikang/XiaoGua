from models import User
from models import Weibo

from response import session
from response import template
from response import response_with_headers
from response import redirect
from response import error

from utils import log


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username

# 微博相关页面
def route_weibo_index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    # username = current_user(request)
    # if username == '游客':
    #     # 没登录 不让看 重定向到 /
    #     return redirect('/login')
    # else:
    header = response_with_headers(headers)
    user_id = request.query.get('user_id', -1)
    user_id = int(user_id)
    user = User.find(user_id)
    if user is None:
        return error(request)
    # 找到 user 发布的所有 weibo
    weibos = Weibo.find_all(user_id=user_id)
    log('weibos', weibos)
    def weibo_tag(weibo):
        return '<p>{} from {}@{} <a href="/weibo/delete?id={}">删除</a> <a href="/weibo/edit?id={}">修改</a></p>'.format(
            weibo.content,
            user.username,
            weibo.created_time,
            weibo.id,
            weibo.id,
        )
    weibos = '\n'.join([weibo_tag(w) for w in weibos])
    body = template('weibo_index.html', weibos=weibos)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_weibo_new(request):
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    header = response_with_headers(headers)
    user = User.find_by(username=username)
    body = template('weibo_new.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_weibo_add(request):
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    header = response_with_headers(headers)
    user = User.find_by(username=username)
    # 创建微博
    form = request.form()
    w = Weibo(form)
    w.user_id = user.id
    w.save()
    return redirect('/weibo?user_id={}'.format(user.id))


def route_weibo_delete(request):
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    header = response_with_headers(headers)
    user = User.find_by(username=username)
    # 删除微博
    weibo_id = request.query.get('id', None)
    weibo_id = int(weibo_id)
    w = Weibo.find(weibo_id)
    w.delete()
    return redirect('/weibo?user_id={}'.format(user.id))


def route_weibo_edit(request):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    weibo_id = request.query.get('id', -1)
    weibo_id = int(weibo_id)
    w = Weibo.find(weibo_id)
    if w is None:
        return error(request)
    # 生成一个 edit 页面
    body = template('weibo_edit.html',
                    weibo_id=w.id,
                    weibo_content=w.content)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_weibo_update(request):
    username = current_user(request)
    user = User.find_by(username=username)
    form = request.form()
    content = form.get('content', '')
    weibo_id = int(form.get('id', -1))
    w = Weibo.find(weibo_id)
    if user.id != w.user_id:
        return error(request)
    w.content = content
    w.save()
    # 重定向到用户的主页
    return redirect('/weibo?user_id={}'.format(user.id))


# 定义一个函数统一检测是否登录
def login_required(route_function):
    def func(request):
        username = current_user(request)
        log('登录鉴定', username)
        if username == '游客':
            # 没登录 不让看 重定向到 /login
            return redirect('/login')
        return route_function(request)
    return func


route_dict = {
    '/weibo': route_weibo_index,
    '/weibo/new': login_required(route_weibo_new),
    '/weibo/add': login_required(route_weibo_add),
    '/weibo/delete': login_required(route_weibo_delete),
    '/weibo/edit': login_required(route_weibo_edit),
    '/weibo/update': login_required(route_weibo_update),
}
