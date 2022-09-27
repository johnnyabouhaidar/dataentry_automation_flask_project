from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='mssql://johnny:pass123456@localhost\SQLEXPRESS02/Flask_DataEntry_DB'
app.config['SECRET_KEY']='thisisasecretkey'


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