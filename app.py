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
from report_test import *
import pandas as pd

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
    access=db.Column(db.String(500),nullable=False)



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

class Facturationtype(db.Model):
    facturationtypeid = db.Column(db.Integer,primary_key=True)
    facturationType = db.Column(db.String(80),nullable=False)

class Facturation(db.Model):
    facturationId = db.Column(db.Integer,primary_key=True)
    facturationType = db.Column(db.String(80),nullable=False)
    facturationNom = db.Column(db.String(80),nullable=False)
    somme = db.Column(db.Float,nullable=False)
    date = db.Column(db.Date,nullable=False)


class Dentisterietype(db.Model):
    dentisterietypeId=db.Column(db.Integer,primary_key=True)
    dentisterietype = db.Column(db.String(80),nullable=False)

class Dentisterie(db.Model):
    dentisterieId = db.Column(db.Integer,primary_key=True)
    dentisterieType = db.Column(db.String(80),nullable=False)
    dentisterieNom = db.Column(db.String(80),nullable=False)
    somme=db.Column(db.Float,nullable=False)
    date=db.Column(db.Date,nullable=False)






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

@app.route('/dentisterie',methods=['GET','POST'])
@login_required
def dentisterie():
    form=AddDentistryInfoForm()
    choices=[]
    choices.append(("---","---"))
    choices=choices+[(denttype.dentisterietype,denttype.dentisterietype)for denttype in db.engine.execute("select * from dentisterietype").fetchall()]   
    form.dentisterieType.choices=choices
    form.dentisterieNom.choices= [(dentname.dentisterieId,dentname.dentisterieNom) for dentname in Dentisterie.query.filter_by(dentisterieType='---').all()]
    dentisterie=db.engine.execute("select * from dentisterie")
    dentisterieitems=dentisterie.fetchall()
    headersdentisterie=dentisterie.keys()
    if form.is_submitted() and request.method=='POST':

        if form.dentisterieNom.data!="addnew":
            new_dentisterie =Dentisterie(dentisterieType=form.dentisterieType.data,dentisterieNom=form.dentisterieNom.data,somme=form.somme.data,date=form.date.data)
        else:
            new_dentisterie =Dentisterie(dentisterieType=form.dentisterieType.data,dentisterieNom=form.dentisterieNomALT.data,somme=form.somme.data,date=form.date.data)
        if isinstance(form.somme.data, int) or isinstance(form.somme.data, float):
            db.session.add(new_dentisterie)
            db.session.commit()
            return redirect(url_for('dentisterie'))
        else:
            flash("Invalid Data. Please re-check and submit again")
    
    if "dentisterie" in current_user.access or current_user.access=="all":
        return render_template('generalform.html',form=form,hasDynamicSelector=True,table=dentisterieitems,headers=headersdentisterie,dbtable="dentisterie",dbtableid="dentisterieId",user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')    

@app.route('/dentisterienames/<dentisterietype>')
def dentisterienames(dentisterietype):
    dentisterienames = Dentisterie.query.filter_by(dentisterieType=dentisterietype).all()
    
    dentisterieArry=[]
    for dentisterie in dentisterienames:
        
        if not any(obj['name'] == dentisterie.dentisterieNom for obj in dentisterieArry):
            
            dentisterieObj={}
            dentisterieObj['id']=dentisterie.dentisterieId
            dentisterieObj['name']=dentisterie.dentisterieNom
            dentisterieArry.append(dentisterieObj)
            

    return jsonify({'dentisterienames':dentisterieArry})


@app.route('/facturation',methods=['GET','POST'])
@login_required
def facturation():
    form = AddFacturationForm()
    choices=[]
    choices.append(("---","---"))
    choices=choices+[(facttype.facturationType,facttype.facturationType)for facttype in db.engine.execute("select * from facturationtype").fetchall()]
    form.facturationType.choices = choices
    form.facturationNom.choices= [(factname.facturationId,factname.facturationNom) for factname in Facturation.query.filter_by(facturationType='---').all()]
    facturations=db.engine.execute("select * from facturation")
    facturationsitems=facturations.fetchall()
    headersfacturations=facturations.keys()

    if form.is_submitted() and request.method=='POST':

        if form.facturationNom.data!="addnew":
            new_facturation =Facturation(facturationType=form.facturationType.data,facturationNom=form.facturationNom.data,somme=form.somme.data,date=form.date.data)
        else:
            new_facturation =Facturation(facturationType=form.facturationType.data,facturationNom=form.facturationNomALT.data,somme=form.somme.data,date=form.date.data)
        if isinstance(form.somme.data, int) or isinstance(form.somme.data, float):
            db.session.add(new_facturation)
            db.session.commit()
            return redirect(url_for('facturation'))
        else:
            flash("Invalid Data. Please re-check and submit again")
    

    if "facturation" in current_user.access or current_user.access=="all":
        return render_template('generalform.html',form=form,hasDynamicSelector=True,table=facturationsitems,headers=headersfacturations,dbtable="facturation",dbtableid="facturationId",user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')

@app.route('/facturationnames/<facturationtype>')
def facturationnames(facturationtype):
    facturationnames = Facturation.query.filter_by(facturationType=facturationtype).all()
    
    facturationArry=[]
    for facturation in facturationnames:
        
        if not any(obj['name'] == facturation.paiementsNom for obj in facturationArry):
            
            facturationObj={}
            facturationObj['id']=facturation.facturationId
            facturationObj['name']=facturation.facturationNom
            facturationArry.append(facturationObj)
            

    return jsonify({'facturationnames':facturationArry})

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
            new_payment =Payment(paiementsType=form.paiementsType.data,paiementsNom=form.paiementsNom.data,somme=form.somme.data,date=form.date.data)
        else:
            new_payment =Payment(paiementsType=form.paiementsType.data,paiementsNom=form.paiementsNomALT.data,somme=form.somme.data,date=form.date.data)
        if isinstance(form.somme.data, int) or isinstance(form.somme.data, float):
            db.session.add(new_payment)
            db.session.commit()
            return redirect(url_for('payment'))
        else:
            flash("Invalid Data. Please re-check and submit again")
    
    if "payments" in current_user.access or current_user.access=="all":
        return render_template('generalform.html',form=form,hasDynamicSelector=True,table=paymentitems,headers=headerspayments,dbtable="payment",dbtableid="paiementsId",user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')

@app.route('/paymentnames/<paymenttype>')
def paymentnames(paymenttype):
    paymentnames = Payment.query.filter_by(paiementsType=paymenttype).all()
    
    paymentArry=[]
    for payment in paymentnames:
        
        if not any(obj['name'] == payment.paiementsNom for obj in paymentArry):
            
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
    if "doctors" in current_user.access  or current_user.access=="all":
        return render_template('generalform.html',form=form,hasDynamicSelector=False,table=doctoritems,headers=headersdoctors,dbtable="doctor",dbtableid="doctorId",user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')



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
    if tbl=='payment':
        qry = Payment.query.filter(
            Payment.paiementsId==id).first()
        #doc = qry.first()
        
        form=AddPaymentForm(obj=qry)
        choices=[(paytype.paiementsType,paytype.paiementsType)for paytype in db.engine.execute("select * from paymenttype").fetchall()]
        form.paiementsType.choices = choices
        
        form.paiementsNom.choices=[(qry.paiementsNom,qry.paiementsNom)]
        
        if form.validate_on_submit():
            #qry.doctorid = form.doctorid.data
            qry.paiementsType=form.paiementsType.data
            if form.paiementsNomALT.data=="":
                qry.paiementsNom = form.paiementsNom.data
            else:
                qry.paiementsNom = form.paiementsNomALT.data
            qry.somme=form.somme.data
            qry.date=form.date.data
            
            #qry=form
            db.session.commit()
            return redirect(url_for('payment'))
        else:
            flash("Invalid Data. Please re-check and submit again")
    if tbl=='facturation':
        qry = Facturation.query.filter(
            Facturation.facturationId==id).first()
        #doc = qry.first()
        
        form=AddFacturationForm(obj=qry)
        choices=[(facttype.facturationType,facttype.facturationType)for facttype in db.engine.execute("select * from facturationtype").fetchall()]
        form.facturationType.choices = choices
        
        form.facturationNom.choices=[(qry.facturationNom,qry.facturationNom)]
        
        if form.validate_on_submit():
            #qry.doctorid = form.doctorid.data
            qry.facturationType=form.facturationType.data
            if form.facturationNomALT.data=="":
                qry.facturationNom = form.facturationNom.data
            else:
                qry.facturationNom = form.facturationNomALT.data
            qry.somme=form.somme.data
            qry.date=form.date.data
            
            #qry=form
            db.session.commit()
            return redirect(url_for('facturation'))
    if tbl=='dentisterie':
        qry = Dentisterie.query.filter(
            Dentisterie.dentisterieId==id).first()
        #doc = qry.first()
        
        form=AddDentistryInfoForm(obj=qry)
        choices=[(facttype.dentisterietype,facttype.dentisterietype)for facttype in db.engine.execute("select * from dentisterietype").fetchall()]
        form.dentisterieType.choices = choices
        
        form.dentisterieNom.choices=[(qry.dentisterieNom,qry.dentisterieNom)]
        
        if form.validate_on_submit():
            #qry.doctorid = form.doctorid.data
            
            qry.dentisterieType=form.dentisterieType.data
            if form.dentisterieNomALT.data == "":
                qry.dentisterieNom = form.dentisterieNom.data
            else:
                qry.dentisterieNom = form.dentisterieNomALT.data
            qry.somme=form.somme.data
            qry.date=form.date.data
            
            #qry=form
            db.session.commit()
            return redirect(url_for('dentisterie'))

    if tbl=='user':
        qry = User.query.filter(
            User.id==id
        ).first()


        
        if qry.role=="admin":
            form=EditRegisterForm(obj=qry,isAdmin=True)
        else:
            form=EditRegisterForm(obj=qry,isAdmin=False)
        form.access.data = qry.access.split(" ")
        if form.validate_on_submit():
            #qry.doctorid = form.doctorid.data
            form.access.data=None
            
            rolesstr=" "
            qry.username=form.username.data
            qry.password = form.password.data
            if form.isAdmin.data:
                qry.role="admin"
            else:
                qry.role="user"

            qry.access=rolesstr.join(request.form.getlist('access'))
            
            #new_user = User(username=form.username.data,password=form.password.data,role="user",access=rolesstr.join(form.access.data))
            #qry=form
            db.session.commit()
            return redirect(url_for('user'))
        else:
            print(form.errors)
        

    return render_template('edititem.html',form=form)



@app.route('/delete_entry/tbl=<tbl>/tblid=<tblid>/id=<id>',methods=['GET','POST'])
@login_required
def delete_entry(tbl,tblid,id):
    db.engine.execute("delete from \"{0}\" where {1}={2}".format(tbl,tblid,id))
    db.session.commit()
    if 'type' in tbl:
        return redirect(url_for('setup'))
    else:
        return redirect(url_for(tbl))



@app.route('/user',methods=['GET','POST'])
def user():
    form=RegisterForm()
    userlslist=db.engine.execute("select * from \"user\"")
    userlslistitems=userlslist.fetchall()
    headersuserlslist=userlslist.keys()
    if form.validate_on_submit():
        password=form.password.data
        #hashed_password= Bcrypt.generate_password_hash(password)
        rolesstr=" "
        if form.isAdmin.data:
            new_user = User(username=form.username.data,password=form.password.data,role="admin",access=rolesstr.join(form.access.data))
        else:
            new_user = User(username=form.username.data,password=form.password.data,role="user",access=rolesstr.join(form.access.data))
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    if current_user.role=="admin":
        return render_template("user.html",form=form,table=userlslistitems,headers=headersuserlslist,user_role=current_user.role,dbtable="user",dbtableid="id")
    else:
        return render_template("NOT_AUTHORIZED.html")

@app.route('/reporting',methods=['GET','POST'])
@login_required
def reporting():
    #paymentslist=db.engine.execute("""SELECT paiementsNom,SUM(somme) AS somme FROM payment GROUP BY paiementsNom;""")
    paymentslist=db.engine.execute("""select paiementsType, SUM(somme) AS somme ,MONTH(date) AS "month",YEAR(date) as "year" From payment where YEAR(date)>2021 group by YEAR(date),MONTH(date) , paiementsType """)
    #paymentslist=db.engine.execute("SELECT *from payment")
    paymentslistitems=paymentslist.fetchall()
    headerspaymentslist=paymentslist.keys()
    paymentdf = pd.DataFrame(paymentslistitems,columns=headerspaymentslist)
    #generate_payment_report(paymentdf)
    paymentdf.set_index('paiementsType',inplace=True)
    dataframe_to_pdf(paymentdf,'sample.pdf')
    #print(paymentdf)
    if "reports" in current_user.access  or current_user.access=="all":
        return send_file('sample.pdf')
    else:
        return render_template("NOT_AUTHORIZED.html")
    

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

    form2 =AddFacturationtype()
    facturationtypes=db.engine.execute("select * from facturationtype")
    facturationtypesitems=facturationtypes.fetchall()
    headersfacturationtypes=facturationtypes.keys()
    
    if form2.validate_on_submit():
        new_facturation_type =Facturationtype(facturationType=form2.facturationtype.data)
        db.session.add(new_facturation_type)
        db.session.commit()
        return redirect(url_for('setup'))

    form3 = AddDentistrytype()
    dentisterietypes=db.engine.execute("select * from Dentisterietype")
    dentisterietypesitems=dentisterietypes.fetchall()
    headersdentisterietypes=dentisterietypes.keys()

    if form3.validate_on_submit():
        new_dentisterie_type=Dentisterietype(dentisterietype=form3.dentisterieType.data)
        db.session.add(new_dentisterie_type)
        db.session.commit()
        return redirect(url_for('setup'))


    if "setup" in current_user.access  or current_user.access=="all":        
        return render_template('setup.html',forms=[form1,form2,form3],table=[paymenttypesitems,facturationtypesitems,dentisterietypesitems],headers=[headerspaymenttypes,headersfacturationtypes,headersdentisterietypes],dbtable=["paymenttype","facturationtype","dentisterietype"],dbtableid=["paiementstypeid","facturationtypeid","dentisterietypeid"],user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')



@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0")