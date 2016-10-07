from . import ModelMixin
from . import db
from . import timestamp


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))

    #
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))

    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
