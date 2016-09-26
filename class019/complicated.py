from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///complicated.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class ReprMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))


class Message(db.Model, ReprMixin):
    """
    消息是用户发给用户的, 相当于私信
    有一个发送者 id
    有一个所有者 id
    """
    __tablename__ = 'msgs'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    sender_id = db.Column(db.String(), db.ForeignKey('users.id'))
    owner_id = db.Column(db.String(), db.ForeignKey('users.id'))

    def __init__(self, content):
        self.content = content


class User(db.Model, ReprMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    # 用户可以有两种不同的关联
    sends = db.relationship('Message', backref='sender', foreign_keys='Message.sender_id')
    owns = db.relationship('Message', backref='owner', foreign_keys='Message.owner_id')

    def __init__(self, name):
        self.username = name


def test_add():
    u1 = User('gua1')
    u1.save()
    u2 = User('gua2')
    u2.save()
    m1 = Message('thank you')
    # 当然 直接写 sender_id 的值也是可以的
    m1.sender = u1
    m1.owner = u2
    m1.save()


def test_query():
    ms = Message.query.all()
    m = ms[0]
    print('message test', m.content, m.sender.username, m.owner.username)


if __name__ == '__main__':
    # manager.run()
    # test_add()
    test_query()
