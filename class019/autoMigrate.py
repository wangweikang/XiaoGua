from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autoMigrate.sqlite'
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    sex = db.Column(db.String())


def test():
    u = User()
    u.name = 'gua 1'
    u.sex = 'male'
    u.save()
    us = User.query.all()
    print(us)


if __name__ == '__main__':
    manager.run()
    # test()
