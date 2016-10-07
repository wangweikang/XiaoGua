from models.comment import Comment
from routes import *


main = Blueprint('comment', __name__)

Model = Comment

#
# @main.route('/')
# def index():
#     ms = Model.query.all()
#     return render_template('topic_index.html', node_list=ms)


# @main.route('/new')
# def new():
#     return render_template('topic_new.html')


# @main.route('/<int:id>')
# def show(id):
#     m = Model.query.get(id)
#     return render_template('topic.html', topic=m)


# @main.route('/edit/<id>')
# def edit(id):
#     t = Model.query.get(id)
#     return render_template('topic_edit.html', todo=t)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Model(form)
    m.topic_id = int(form.get('topic_id'))
    m.save()
    return redirect(url_for('topic.show', id=m.topic_id))


# @main.route('/update/<int:id>', methods=['POST'])
# def update(id):
#     form = request.form
#     t = Model.query.get(id)
#     t.update(form)
#     return redirect(url_for('.index'))
#
#
# @main.route('/delete/<int:id>')
# def delete(id):
#     t = Model.query.get(id)
#     t.delete()
#     return redirect(url_for('.index'))
