from models import Todo

from response import session
from response import template
from response import response_with_headers
from response import redirect
from response import error

from utils import log


# def current_user(request):
#     session_id = request.cookies.get('user', '')
#     username = session.get(session_id, '游客')
#     return username

def route_index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    todos = Todo.all()
    log('todos', todos)
    def todo_tag(t):
        status = t.status()
        return '<p class="{}">{} {}@{}<a href="/todo/complete?id={}">完成</a></p>'.format(
            status,
            t.id,
            t.content,
            t.created_time,
            t.id,
        )
    todo_html = '\n'.join([todo_tag(t) for t in todos])
    body = template('todo_index.html', todos=todo_html)
    # log('todo', body)
    # log('')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_add(request):
    # headers = {
    #     'Content-Type': 'text/html',
    # }
    # 创建微博
    form = request.form()
    o = Todo(form)
    o.save()
    return redirect('/todo')


def route_complete(request):
    headers = {
        'Content-Type': 'text/html',
    }
    # username = current_user(request)
    # header = response_with_headers(headers)
    # user = User.find_by(username=username)
    # 删除微博
    id = int(request.query.get('id', -1))
    o = Todo.find(id)
    o.toggleComplete()
    o.save()
    return redirect('/todo')
#
#
# def route_weibo_edit(request):
#     headers = {
#         'Content-Type': 'text/html',
#     }
#     header = response_with_headers(headers)
#     weibo_id = request.query.get('id', -1)
#     weibo_id = int(weibo_id)
#     w = Weibo.find(weibo_id)
#     if w is None:
#         return error(request)
#     # 生成一个 edit 页面
#     body = template('weibo_edit.html',
#                     weibo_id=w.id,
#                     weibo_content=w.content)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')
#
#
# def route_weibo_update(request):
#     username = current_user(request)
#     user = User.find_by(username=username)
#     form = request.form()
#     content = form.get('content', '')
#     weibo_id = int(form.get('id', -1))
#     w = Weibo.find(weibo_id)
#     if user.id != w.user_id:
#         return error(request)
#     w.content = content
#     w.save()
#     # 重定向到用户的主页
#     return redirect('/weibo?user_id={}'.format(user.id))


# 定义一个函数统一检测是否登录
# def login_required(route_function):
#     def func(request):
#         username = current_user(request)
#         log('登录鉴定', username)
#         if username == '游客':
#             # 没登录 不让看 重定向到 /login
#             return redirect('/login')
#         return route_function(request)
#     return func


route_dict = {
    '/todo': route_index,
    # '/todo/new': login_required(route_weibo_new),
    '/todo/add': route_add,
    '/todo/complete': route_complete,
    # '/todo/delete': route_delete,
    # '/todo/edit': login_required(route_weibo_edit),
    # '/todo/update': login_required(route_weibo_update),
}
