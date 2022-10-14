from DB_layer import *
from flask import Flask, render_template, url_for,redirect, flash,send_file, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,Label,BooleanField
from wtforms.validators import InputRequired,Length,ValidationError,DataRequired
from flask_bcrypt import Bcrypt
from forms import *
import datetime
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



class Doctor(db.Model):
    doctorid=db.Column(db.Integer,primary_key=True)
    doctorname=db.Column(db.String(80),nullable=False,unique=True)
    doctorspeciality=db.Column(db.String(80),nullable=False)
    isActive = db.Column(db.Boolean,nullable=False)
    percentageShare = db.Column(db.Float,nullable=False)


class Paymenttype(db.Model):
    paiementstypeid = db.Column(db.Integer,primary_key=True)
    paiementsType = db.Column(db.String(80),nullable=False)  


class Payment(db.Model):
    paiementsId = db.Column(db.Integer,primary_key=True)
    paiementsType = db.Column(db.String(80),nullable=False)
    paiementsNom = db.Column(db.String(80),nullable=False)
    somme = db.Column(db.Float,nullable=False)
    date = db.Column(db.Date,nullable=False)






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
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect credentials")
        else:
            flash("Incorrect credentials")
    return render_template("login.html",form=form)



@app.route('/dashboard',methods=['GET','POST'])
#@app.route('/dashboard/usr=<usr>',methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html',username=current_user.username,user_role=current_user.role)



@app.route('/payments',methods=['GET','POST'])
@login_required
def payment():
    form=AddPaymentForm()
    choices=[]
    choices.append(("---","---"))
    choices=choices+[(paytype.paiementsType,paytype.paiementsType)for paytype in db.engine.execute("select * from paymenttype").fetchall()]
    #choices.append((paytype.paiementsType,paytype.paiementsType)for paytype in db.engine.execute("select * from paymenttype").fetchall())
    
    form.paiementsType.choices = choices
    form.paiementsNom.choices= [(payname.paiementsId,payname.paiementsNom) for payname in Payment.query.filter_by(paiementsType='---').all()]

    payments=db.engine.execute("select * from payment")
    paymentitems=payments.fetchall()
    headerspayments=payments.keys()
    
    if form.is_submitted() and request.method=='POST':
        if form.paiementsNom.data!="addnew":
            new_payment =Payment(paiementsType=form.paiementsType.data,paiementsNom=form.paiementsNom.data,somme=form.somme.data,date=form.Date.data)
        else:
            new_payment =Payment(paiementsType=form.paiementsType.data,paiementsNom=form.paiementsNomALT.data,somme=form.somme.data,date=form.Date.data)
        db.session.add(new_payment)
        db.session.commit()
        return redirect(url_for('payment'))
    

    return render_template('generalform.html',form=form,hasDynamicSelector=True,table=paymentitems,headers=headerspayments,dbtable="payment",dbtableid="paiementsId",user_role=current_user.role)

@app.route('/paymentnames/<paymenttype>')
def paymentnames(paymenttype):
    paymentnames = Payment.query.filter_by(paiementsType=paymenttype).all()

    paymentArry=[]
    for payment in paymentnames:
        paymentObj={}
        paymentObj['id']=payment.paiementsId
        paymentObj['name']=payment.paiementsNom
        paymentArry.append(paymentObj)

    return jsonify({'paymentnames':paymentArry})

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
    return render_template('generalform.html',form=form,hasDynamicSelector=False,table=doctoritems,headers=headersdoctors,dbtable="doctor",dbtableid="doctorId",user_role=current_user.role)



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



@app.route('/delete_entry/tbl=<tbl>/tblid=<tblid>/id=<id>',methods=['GET','POST'])
@login_required
def delete_entry(tbl,tblid,id):
    db.engine.execute("delete from {0} where {1}={2}".format(tbl,tblid,id))
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

@app.route('/returnfile',methods=['GET','POST'])
@login_required
def returnfile():
    return send_file('sample.pdf')

@app.route('/setup',methods=['GET','POST'])
@login_required
def setup():
    form1 =Addpaymenttype()
    paymenttypes=db.engine.execute("select * from paymenttype")
    paymenttypesitems=paymenttypes.fetchall()
    headerspaymenttypes=paymenttypes.keys()
    
    if form1.validate_on_submit():
        new_payment_type =Paymenttype(paiementsType=form1.paymenttype.data)
        db.session.add(new_payment_type)
        db.session.commit()
        return redirect(url_for('setup'))
    return render_template('setup.html',forms=[form1],table=[paymenttypesitems],headers=[headerspaymenttypes],dbtable=["paymenttype"],dbtableid=["paiementstypeid"],user_role=current_user.role)



@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0")