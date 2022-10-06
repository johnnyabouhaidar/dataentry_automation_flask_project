from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,Label,BooleanField
from app import *

class Payment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    paymenttype=db.Column(db.String(80),nullable=False)
    paymentdate=db.Column(db.String(80),nullable=False)
    amount = db.Column(db.String(80),nullable=False)
    currency = db.Column(db.String(80),nullable=False)