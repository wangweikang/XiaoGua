import time

from . import ModelMixin
from . import db


class Todo(db.Model, ModelMixin):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String())
    created_time = db.Column(db.Integer)
    updated_time = db.Column(db.Integer)
    # 这是一个外键
    # user_id = db.Column(db.Integer, db.ForeignKey('stb_users.id'))
    # # relationship
    # reviews = db.relationship('Review', backref='chest')

    def __init__(self, form):
        print('chest init', form)
        self.task = form.get('task', '')
        self.created_time = int(time.time())

    def update(self, form):
        self.task = form.get('task', '')
        self.save()
