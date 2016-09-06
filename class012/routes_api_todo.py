from models import Todo

from response import session
from response import template
from response import response_with_headers
from response import redirect
from response import error

from utils import log


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
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    # 创建微博
    form = request.form()
    o = Todo(form)
    o.save()
    body = o.json_str()
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


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

route_dict = {
    '/api/todo': route_index,
    '/api/todo/add': route_add,
    '/api/todo/complete': route_complete,
    # '/todo/delete': route_delete,
    # '/todo/edit': login_required(route_weibo_edit),
    # '/todo/update': login_required(route_weibo_update),
}
