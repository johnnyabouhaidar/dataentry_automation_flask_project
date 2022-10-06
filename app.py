from DB_layer import *
from flask import Flask, render_template, url_for,redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,Label,BooleanField
from wtforms.validators import InputRequired,Length,ValidationError,DataRequired
from flask_bcrypt import Bcrypt
from doctorslist import *
#from pandas import pd

#from UserClass import *

app = Flask(__name__)



db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
#app.config['SQLALCHEMY_DATABASE_URI']='mssql+pyodbc://johnny:pass123456@localhost\SQLEXPRESS02/Flask_DataEntry_DB?driver=sql+server?trusted_connection=yes'
#app.config['SQLALCHEMY_DATABASE_URI']=f"mssql+pyodbc://flask1:flaskPass@localhost\SQLEXPRESS/Flask_DataEntry_DB?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_DATABASE_URI']=f"mssql+pyodbc://johnny:pass123456@localhost\SQLEXPRESS02/Flask_DataEntry_DB?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SECRET_KEY']='thisisasecretkey'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False, unique=True)
    password = db.Column(db.String(80),nullable=False)
    role = db.Column(db.String(50),nullable=False)





class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})

    submit =SubmitField("Register")

    def validate_username(self,username):
        existing_user_username = User.query.filter_by(
            username=username.data
        ).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )
class LoginForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})

    submit=SubmitField("Login")


@app.route('/')
def home():
    #return render_template("welcome.html")
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password==form.password.data:
                login_user(user)
                return redirect(url_for('dashboard',usr=user.username))
            else:
                flash("Incorrect credentials")
        else:
            flash("Incorrect credentials")
    return render_template("login.html",form=form)

@app.route('/dashboard',methods=['GET','POST'])
#@app.route('/dashboard/usr=<usr>',methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html',username=current_user.username)

@app.route('/doctors',methods=['GET','POST'])
@login_required
def doctor():
    form=AddDoctorForm()
    doctors=db.engine.execute("select * from doctor")
    doctoritems=doctors.fetchall()
    headersdoctors=doctors.keys()
    
    if form.validate_on_submit():
        #boolean = False
        #if form.isActive.data=='True':
            #boolean = True
        new_doctor =Doctor(doctorname=form.doctorname.data,doctorspeciality=form.doctorspeciality.data,isActive=form.isActive.data,percentageShare=form.percentageShare.data)
        db.session.add(new_doctor)
        db.session.commit()
        return redirect(url_for('doctor'))
    #return render_template('doctorregisterform.html',form=form,tables=[doctors.to_html(classes='data',index=False)], titles=doctors.columns.values)
    return render_template('doctorregisterform.html',form=form,table=doctoritems,headers=headersdoctors,dbtable="doctor",user_role=current_user.role)

@app.route('/edit_entry/tbl=<tbl>/id=<id>',methods=['GET','POST'])
@login_required
def edit_entry(tbl,id):
    if tbl=='doctor':
        qry = Doctor.query.filter(
            Doctor.doctorid==id).first()
        #doc = qry.first()
        
        form=AddDoctorForm(obj=qry)
        if form.validate_on_submit():
            #qry.doctorid = form.doctorid.data
            qry.doctorname=form.doctorname.data
            qry.isActive = form.isActive.data
            qry.doctorspeciality=form.doctorspeciality.data
            qry.percentageShare=form.percentageShare.data
            
            #qry=form
            db.session.commit()
            return redirect(url_for('doctor'))
    return render_template('edititem.html',form=form)

@app.route('/delete_entry/tbl=<tbl>/id=<id>',methods=['GET','POST'])
@login_required
def delete_entry(tbl,id):
    db.engine.execute("delete from {0} where doctorid={1}".format(tbl,id))
    db.session.commit()
    return redirect(url_for(tbl))

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():

        password=form.password.data
        #hashed_password= Bcrypt.generate_password_hash(password)

        new_user = User(username=form.username.data,password=form.password.data,role="user")
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html",form=form)

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)