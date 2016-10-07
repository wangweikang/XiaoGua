from models.user import User
# from models.topic import Topic
from routes import *

# for decorators
from functools import wraps


main = Blueprint('auth', __name__)

Model = User


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        # your code
        print('admin required')
        if request.args.get('uid') != '1':
            print('not admin')
            abort(404)
        return f(*args, **kwargs)
    return function


@main.route('/')
def index():
    # ms = Model.query.all()
    return render_template('auth_index.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    user = Model.query.filter_by(username=u.username).first()
    if u.valid_login(user):
        session.permanent = True
        session['uid'] = user.id
        return redirect('/nodes')
    else:
        return redirect(url_for('.index'))


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    if u.valid():
        u.save()
        session.permanent = True
        session['uid'] = u.id
        return redirect('/')
    else:
        return redirect(url_for('.index'))
