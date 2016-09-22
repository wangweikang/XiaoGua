from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import time
import json
import datetime

# 以下都是套路
app = Flask(__name__)
app.secret_key = 'qweqadasdafasrwqaerxcvzv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 指定数据库的路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

db = SQLAlchemy(app)


# 定义一个 Model，继承自 db.Model

class ModelHelper(object):
    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Weibo(db.Model, ModelHelper):
    __tablename__ = 'weibos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    weibo = db.Column(db.String())
    name = db.Column(db.String())
    created_time = db.Column(db.String(), default=0)

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.weibo = form.get('weibo', '')
        self.name = form.get('name', '')
        self.created_time = dt
        self.comment = ''
        self.comments_num = 0

    def valid(self):
        return len(self.weibo) > 2 and len(self.weibo) < 10 and len(self.name) > 0

    def comments(self):
        cs = Comment.query.filter_by(weibo_id=self.id).all()
        return cs

    def get_avatar(self):
        a = User.query.filter_by(username=self.name).first()
        if a is None:
            return 'http://vip.cocode.cc/uploads/avatar/default.png'
        return a.avatar

    def error_message(self):
        if len(self.weibo) <= 2:
            return '微博太短了，至少要 3 个字符'
        elif len(self.weibo) >= 10:
            return '微博不能大于9个字符'

    def json(self):
        """
        id = db.Column(db.Integer, primary_key=True)
        weibo = db.Column(db.String())
        name = db.Column(db.String())
        created_time = db.Column(db.String(), default=0)


        i.comment = i.comments()
        for j in i.comment:
            j.avatar = j.get_avatar()
        i.comments_num = len(i.comment)
        i.avatar = i.get_avatar()

        """
        d = dict(
            id=self.id,
            weibo=self.weibo,
            name=self.name,
            created_time=self.created_time,
            avatar=self.get_avatar(),
            comments_num=len(self.comments()),
        )
        return d


class Comment(db.Model, ModelHelper):
    __tablename__ = 'comments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String())
    name = db.Column(db.String())
    created_time = db.Column(db.String(), default=0)
    weibo_id = db.Column(db.Integer)

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.comment = form.get('comment', '')
        self.name = form.get('name', '')
        self.weibo_id = form.get('weibo_id', '')
        self.created_time = dt

    def valid(self):
        return len(self.comment) > 0 and len(self.name) > 0

    def get_avatar(self):
        a = User.query.filter_by(username=self.name).first()
        if a is None:
            return 'http://vip.cocode.cc/uploads/avatar/default.png'
        return a.avatar


class User(db.Model, ModelHelper):
    __tablename__ = 'users'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    avatar = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.avatar = form.get('avatar', 'http://vip.cocode.cc/uploads/avatar/default.png')
        self.created_time = int(time.time())

    def weibos(self):
        ws = Weibo.query.filter_by(user_id=self.id).all()
        return ws

    def valid(self):
        user = User.query.filter_by(username=self.username).first()
        if user is not None:
            return False
        return len(self.username) > 2 and len(self.password) > 2

    def validate_login(self, u):
        return u.username == self.username and u.password == self.password

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        else:
            return False

    def change_avatar(self, avatar):
        if len(avatar) > 2:
            self.avatar = avatar
            self.save()
            return True
        else:
            return False


class Blog(db.Model, ModelHelper):
    __tablename__ = 'blogs'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    title = db.Column(db.String())
    name = db.Column(db.String())
    created_time = db.Column(db.String(), default=0)

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.name = form.get('name', '')
        self.created_time = dt
        self.comment = ''
        self.comments_num = 0

    def valid(self):
        return len(self.title) > 0 and len(self.content) > 0

    def comments(self):
        cs = BlogComment.query.filter_by(blog_id=self.id).all()
        return cs


class BlogComment(db.Model, ModelHelper):
    __tablename__ = 'blog_comments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String())
    name = db.Column(db.String())
    created_time = db.Column(db.String(), default=0)
    blog_id = db.Column(db.Integer)

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.comment = form.get('comment', '')
        self.name = form.get('name', '')
        self.blog_id = form.get('blog_id', '')
        self.created_time = dt

    def valid(self):
        return len(self.comment) > 0 and len(self.name) > 0

    def get_avatar(self):
        a = User.query.filter_by(username=self.name).first()
        if a is None:
            return 'http://vip.cocode.cc/uploads/avatar/default.png'
        return a.avatar

    def json(self):
        d = {
            'id': self.id,
            'comment': self.comment,
            'created_time': self.created_time,
            'blog_id': self.blog_id,
            'name': self.name,
            'avatar': self.avatar,
        }
        return json.dumps(d, ensure_ascii=False)


def db_build():
    db.drop_all()
    db.create_all()
    print('rebuild database')


if __name__ == '__main__':
    # 先 drop_all 删除所有数据库中的表
    # 再 create_all 创建所有的表
    db_build()
