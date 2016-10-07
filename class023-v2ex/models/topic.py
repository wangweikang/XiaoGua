from . import ModelMixin
from . import db
from . import timestamp


class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    # has relationship with comments
    comments = db.relationship('Comment', backref="node")

    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
