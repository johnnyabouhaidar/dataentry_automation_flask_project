from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
#from UserClass import *

app = Flask(__name__)



db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='mssql+pyodbc://johnny:pass123456@localhost\SQLEXPRESS02/Flask_DataEntry_DB?driver=sql+server?trusted_connection=yes'
app.config['SECRET_KEY']='thisisasecretkey'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(50),nullable=False)
    role = db.Column(db.String(50),nullable=False)

@app.route('/')
def home():
    return render_template("welcome.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")


if __name__=='__main__':
    app.run(debug=True)