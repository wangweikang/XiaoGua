from models.todo import Todo
from routes import *


main = Blueprint('todo', __name__)

pyid = id
Model = Todo


@main.route('/')
def index():
    ts = Todo.query.all()
    return render_template('todo_index.html', todo_list=ts)


@main.route('/edit/<id>')
def edit(id):
    t = Todo.query.filter_by(id=id).first()
    return render_template('todo_edit.html', todo=t)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    t = Todo(form)
    t.save()
    return redirect(url_for('.index'))


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    # t = Todo.query.filter_by(id=id).first()
    t = Todo.query.get(id)
    t.update(form)
    return redirect(url_for('.index'))


@main.route('/delete/<id>')
def delete(id):
    # Todo.delete(id)
    t = Todo.query.filter_by(id=id).first()
    t.delete()
    return redirect(url_for('.index'))
