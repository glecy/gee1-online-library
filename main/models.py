from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    def set_password(password):
        password = generate_password_hash(password)

class Book(db.Model):
    __bind_key__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), nullable=False)
    author = db.Column(db.String(400), nullable=False)
    url = db.Column(db.String(600), nullable=False)
    topic = db.Column(db.String(20), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Book %r>' % self.id
