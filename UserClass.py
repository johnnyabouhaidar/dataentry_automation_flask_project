from flask_login import UserMixin

class User(db.Model, UserMixin):
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(50),nullable=False)