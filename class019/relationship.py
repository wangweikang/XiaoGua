from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relationship.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# 下面三行是套路, 用来增加迁移的命令
# 迁移就是要这样, 使用是在命令行
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


class User(db.Model, ReprMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    # 定义一个关系
    # 注意, db.relationship 并不是数据库表中的一个字段
    # foreign_keys 有时候可以省略, 比如现在...
    # backref 的值是 Comment 类中引用 User 的属性
    # foreign_keys 指定了我们选择数据的语句
    # 类似于 Comment.query.filter_by(user_id=self.id)
    comments = db.relationship('Comment',
     backref='user',
     lazy='select',
     foreign_keys='Comment.user_id')

    def __init__(self, name):
        self.username = name
"""

4, SQLAlchemy 关系的其他参数
order_by
指定关系中记录的排序方式

lazy 参数指定加载关系数据的方式
    select 用到了才加载, 默认值
    immediate 立即加载
    dynamic 提供查询让用户自行加载
    noload 永不加载
    还有暂时用不到的两个值 joined 和 subquery, 现在不关心
"""

class Comment(db.Model, ReprMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    # 这里要定义外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content):
        self.content = content


def test_add():
    u = User('gua')
    u.save()
    c1 = Comment('hello')
    # 这里也可以直接写值 c1.user_id = u.id
    # 设置 user 是程序自动帮你写值
    c1.user = u
    c1.save()
    c2 = Comment('gw')
    c2.user = u
    c2.save()


def test_query():
    u = User.query.filter_by(username='gua').first()
    # 自动关联 不用手动查询就有数据
    print('user, ', u.__dict__)
    print('user comments', u.comments, type(u.comments))
    # print('user comments', u.comments.all())
    print('user, ', u.__dict__)


if __name__ == '__main__':
    # test_add()
    test_query()
    # manager.run()
