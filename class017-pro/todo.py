from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort

from models import Todo

from gualib import log


# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('todo', __name__)


@main.route('/')
def index():
    # 查找所有的 todo 并返回
    todo_list = Todo.query.all()
    return render_template('todo_index.html', todos=todo_list)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    t = Todo(form)
    if t.valid():
        t.save()
    else:
        abort(400)
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 todo
    return redirect(url_for('todo.index'))


@main.route('/delete/<int:todo_id>')
def delete(todo_id):
    """
    <int:todo_id> 的方式可以匹配一个 int 类型
    int 指定了它的类型，省略的话参数中的 todo_id 就是 str 类型

    这个概念叫做 动态路由
    意思是这个路由函数可以匹配一系列不同的路由

    动态路由是现在流行的路由设计方案
    """
    # 通过 id 查询 todo 并返回
    t = Todo.query.get(todo_id)
    # 删除
    t.delete()
    # 引用蓝图内部的路由函数的时候，可以省略名字只用 .
    return redirect(url_for('.index'))


# TODO 的完善，增加一个修改 todo 的功能
# 1，todo_index.html 模板中增加一个链接
# 	链接跳转到 /todo/edit/<todo_id>
# 	注意，/todo 前缀在蓝图注册的时候添加了所以不要重复写
# 2，/todo/edit/<todo_id> 返回一个 todo_edit.html 页面
# 	修改的表单发送到 /todo/update/<todo_id>
# 3，新增一个 /todo/update/<todo_id> 路由
# 	接受一个表单包含了修改后的 todo.task
# 	修改这个 todo 并 redirect 到 /todo
