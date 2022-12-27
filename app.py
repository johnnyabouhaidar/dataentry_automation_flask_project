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
from report import *
from doctor_report import *
import pandas as pd

#from UserClass import *

app = Flask(__name__)



db=SQLAlchemy()
bcrypt = Bcrypt(app)
#app.config['SQLALCHEMY_DATABASE_URI']='mssql+pyodbc://johnny:pass123456@localhost\SQLEXPRESS02/Flask_DataEntry_DB?driver=sql+server?trusted_connection=yes'


#app.config['SQLALCHEMY_DATABASE_URI']=f"mssql+pyodbc://flask1:flaskPass@localhost\SQLEXPRESS/Flask_DataEntry_DB?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_DATABASE_URI']=f"mssql+pyodbc://johnny:pass123456@localhost\SQLEXPRESS02/Flask_DataEntry_DB?driver=ODBC+Driver+17+for+SQL+Server"

db.init_app(app)
app.config['SECRET_KEY']='thisisasecretkeyjohnny'


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
    conditionsfinanciers=db.Column(db.String(250),nullable=False)

    surfacecentremedical = db.Column(db.Float)
    surfacecommunes=db.Column(db.Float)
    loyermensuel=db.Column(db.Float)
    surfaceaccordee=db.Column(db.Float)
    nettoyage=db.Column(db.Float)
    conciergerie=db.Column(db.Float)
    salairepersonnel=db.Column(db.Float)
    telephonieinternet=db.Column(db.Float)
    logicielaxenita=db.Column(db.Float)
    nbmedicins=db.Column(db.Float)
    assurances =db.Column(db.Float)
    blanchisserieleman=db.Column(db.Float)
    informatique=db.Column(db.Float)
    nblocaux=db.Column(db.Float)
    nbmedicinsrepartirfrais=db.Column(db.Float)
    receptionniste=db.Column(db.Float)
    Apprentie=db.Column(db.Float)


class Paymenttype(db.Model):
    paiementstypeid = db.Column(db.Integer,primary_key=True)
    paiementsType = db.Column(db.String(80),nullable=False)  


class Payment(db.Model):
    paiementsId = db.Column(db.Integer,primary_key=True)
    paiementsType = db.Column(db.String(80),nullable=False)
    paiementsNom = db.Column(db.String(80),nullable=False)
    somme = db.Column(db.Float,nullable=False)
    comment = db.Column(db.String(250))
    date = db.Column(db.Date,nullable=False)

class Facturationtype(db.Model):
    facturationtypeid = db.Column(db.Integer,primary_key=True)
    facturationType = db.Column(db.String(80),nullable=False)

class Facturation(db.Model):
    facturationId = db.Column(db.Integer,primary_key=True)
    facturationType = db.Column(db.String(80),nullable=False)
    facturationNom = db.Column(db.String(80),nullable=False)
    somme = db.Column(db.Float,nullable=False)
    comment = db.Column(db.String(250))
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

class Encaissement(db.Model):
    encaissementId=db.Column(db.Integer,primary_key=True)
    encaissementNom=db.Column(db.String(80),nullable=False)
    encaissementDate=db.Column(db.Date,nullable=False)
    montant=db.Column(db.Float,nullable=False)
    banque=db.Column(db.String(80),nullable=False)
    comment = db.Column(db.String(250))


class Doctorpayment(db.Model):
    doctorpaiementId=db.Column(db.Integer,primary_key=True)
    doctorname=db.Column(db.String(80),nullable=False)
    paimentnom=db.Column(db.String(80),nullable=False)
    doctorpaiementsomme=db.Column(db.Float,nullable=False)
    date=db.Column(db.Date,nullable=False)

class Fraismaterieltype(db.Model):
    fraismaterieltypeId=db.Column(db.Integer,primary_key=True)
    fraismaterieltype = db.Column(db.String(80),nullable=False)

class Fraismateriel(db.Model):
    fraismaterielId=db.Column(db.Integer,primary_key=True)
    fraismaterieltype=db.Column(db.String(80),nullable=False)
    fraismaterielnom=db.Column(db.String(80),nullable=False)
    fraismaterielsomme=db.Column(db.Float,nullable=False)
    fraismaterieldate=db.Column(db.Date,nullable=False)

class Leasing(db.Model):
    LeasingId=db.Column(db.Integer,primary_key=True)
    locationNom=db.Column(db.String(80),nullable=False)
    docteur=db.Column(db.String(80),nullable=False)
    debut=db.Column(db.Date,nullable=False)
    finPrevue=db.Column(db.Date,nullable=False)
    paiement=db.Column(db.Float,nullable=True)





@app.route('/')
def home():
    
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


@app.route('/doctorpayment',methods=['GET','POST'])
@login_required
def doctorpayment():
    form=AddDoctorPaymentForm()

    choices=[]
    #choices.append(("---","---"))
    choices=choices+[(doctor.doctorname,doctor.doctorname)for doctor in db.engine.execute("select doctorname from doctor").fetchall()]   
    form.doctorname.choices=choices

    paymentchoices=[]
    paymentchoices.append(("addnew","Ajouter Nouveau ?"))
    paymentchoices=paymentchoices+[(doctorpay.paimentnom,doctorpay.paimentnom)for doctorpay in db.engine.execute("select DISTINCT paimentnom   from doctorpayment").fetchall()]
    form.paimentnom.choices=paymentchoices


    DoctorPayments=db.engine.execute("select * from DoctorPayment")
    DoctorPaymentitems=DoctorPayments.fetchall()
    headersDoctorPayment=DoctorPayments.keys()

    if form.validate_on_submit():
        if form.paimentnom.data=="addnew":
            new_doctorpayment = Doctorpayment(doctorname=form.doctorname.data,paimentnom=form.paimentnomALT.data,doctorpaiementsomme=form.doctorpaiementsomme.data,date=form.date.data)
        else:
            new_doctorpayment = Doctorpayment(doctorname=form.doctorname.data,paimentnom=form.paimentnom.data,doctorpaiementsomme=form.doctorpaiementsomme.data,date=form.date.data)
        db.session.add(new_doctorpayment)
        db.session.commit()
        return redirect(url_for('doctorpayment'))
    else:
        #flash("Invalid Data: ",form.errors)
        pass

    if "paiement_medecin" in current_user.access or current_user.access=="all":
        return render_template('generalform.html',forms=[form],hasDynamicSelector=False,table=DoctorPaymentitems,headers=headersDoctorPayment,dbtable="doctorpayment",dbtableid="doctorpaiementId",user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')

@app.route('/encaissement',methods=['GET','POST'])
@login_required
def encaissement():
    form = AddEncaissementForm()
    export2excel_frm=Export_to_excel()
    encaissementnameschoices = []
    encaissementnameschoices.append(("addnew","Ajouter Nouveau ?"))
    for encname in db.engine.execute("select * from encaissement").fetchall():
        if not any(obj[0] == encname.encaissementNom for obj in encaissementnameschoices):
            encaissementnameschoices.append((encname.encaissementNom,encname.encaissementNom))

    form.encaissementNom.choices = encaissementnameschoices
    encaissements=db.engine.execute("select * from encaissement")
    encaissementitems=encaissements.fetchall()
    headersencaissement=encaissements.keys()
    if form.is_submitted() and request.method=='POST' and form.submit.data:
        if form.encaissementNom.data!="addnew":
            new_encaissement = Encaissement(encaissementNom=form.encaissementNom.data,encaissementDate=form.encaissementDate.data,montant=form.montant.data,banque=form.banque.data,comment=form.comment.data) 
        else:
            new_encaissement = Encaissement(encaissementNom=form.encaissementNomALT.data,encaissementDate=form.encaissementDate.data,montant=form.montant.data,banque=form.banque.data,comment=form.comment.data) 
        if isinstance(form.montant.data,int) or isinstance(form.montant.data,float):
            db.session.add(new_encaissement)
            db.session.commit()
            return redirect(url_for('encaissement'))
        else:
            flash("Invalid Data. Please re-check and submit again")

    encaissementdf=pd.DataFrame(encaissementitems,columns=headersencaissement)
    if export2excel_frm.validate_on_submit() and export2excel_frm.export_submit.data:
        current_date=datetime.datetime.now()
        current_num_timestamp="{0}{1}{2}_{3}{4}{5}".format(current_date.year,current_date.month,current_date.day,current_date.hour,current_date.minute,current_date.second)
        excel_report_path=r"reporting_temporary\ENCAISSEMENT_{}.xlsx".format(current_num_timestamp)
        encaissementdf.to_excel(excel_report_path,index=False)

        return send_file(excel_report_path)

    if "encaissement" in current_user.access or current_user.access=="all":
        return render_template('generalform.html',forms=[form,export2excel_frm],hasDynamicSelector=True,table=encaissementitems,headers=headersencaissement,dbtable="encaissement",dbtableid="encaissementId",user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')


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
        return render_template('generalform.html',forms=[form],hasDynamicSelector=True,table=dentisterieitems,headers=headersdentisterie,dbtable="dentisterie",dbtableid="dentisterieId",user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')    

@app.route('/dentisterienames/<dentisterietype>')
def dentisterienames(dentisterietype):
    dentisterienames = Dentisterie.query.filter_by(dentisterieType=dentisterietype).all()
    doctornames=Doctor.query.all()
    
    Arry=[]
    for dentisterie in dentisterienames:
        
        if not any(obj['name'] == dentisterie.dentisterieNom for obj in Arry):
            
            dentisterieObj={}
            dentisterieObj['id']=dentisterie.dentisterieId
            dentisterieObj['name']=dentisterie.dentisterieNom
            Arry.append(dentisterieObj)
    for doctor in doctornames:
            if not any(obj['name'] == doctor.doctorname for obj in Arry):
                docObj={}
                docObj['id']=doctor.doctorid
                docObj['name']=doctor.doctorname
                Arry.append(docObj)
            

    return jsonify({'dentisterienames':Arry})


@app.route('/facturation',methods=['GET','POST'])
@login_required
def facturation():
    form = AddFacturationForm()
    export2excel_frm=Export_to_excel()
    choices=[]
    choices.append(("---","---"))
    choices=choices+[(facttype.facturationType,facttype.facturationType)for facttype in db.engine.execute("select * from facturationtype").fetchall()]
    form.facturationType.choices = choices
    form.facturationNom.choices= [(factname.facturationId,factname.facturationNom) for factname in Facturation.query.filter_by(facturationType='---').all()]
    facturations=db.engine.execute("select * from facturation order by facturationId DESC")
    facturationsitems=facturations.fetchall()
    headersfacturations=facturations.keys()

    facturationdf=pd.DataFrame(facturationsitems,columns=headersfacturations)
    if export2excel_frm.validate_on_submit() and export2excel_frm.export_submit.data:
        current_date=datetime.datetime.now()
        current_num_timestamp="{0}{1}{2}_{3}{4}{5}".format(current_date.year,current_date.month,current_date.day,current_date.hour,current_date.minute,current_date.second)
        excel_report_path=r"reporting_temporary\FACTURATION_{}.xlsx".format(current_num_timestamp)
        facturationdf.to_excel(excel_report_path,index=False)

        return send_file(excel_report_path)

    if form.is_submitted() and request.method=='POST' and form.submit.data:

        if form.facturationNom.data!="addnew":
            new_facturation =Facturation(facturationType=form.facturationType.data,facturationNom=form.facturationNom.data,somme=form.somme.data,comment=form.comment.data,date=form.date.data)
        else:
            new_facturation =Facturation(facturationType=form.facturationType.data,facturationNom=form.facturationNomALT.data,somme=form.somme.data,comment=form.comment.data,date=form.date.data)
        if isinstance(form.somme.data, int) or isinstance(form.somme.data, float):
            db.session.add(new_facturation)
            db.session.commit()
            return redirect(url_for('facturation'))
        else:
            flash("Invalid Data. Please re-check and submit again")
    

    if "facturation" in current_user.access or current_user.access=="all":
        return render_template('generalform.html',forms=[form,export2excel_frm],hasDynamicSelector=True,table=facturationsitems,headers=headersfacturations,dbtable="facturation",dbtableid="facturationId",user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')

@app.route('/facturationnames/<facturationtype>')
def facturationnames(facturationtype):
    facturationnames = Facturation.query.filter_by(facturationType=facturationtype).all()
    doctornames=Doctor.query.all()
    
    Arry=[]
    for facturation in facturationnames:
        
        if not any(obj['name'] == facturation.facturationNom for obj in Arry):
            
            facturationObj={}
            facturationObj['id']=facturation.facturationId
            facturationObj['name']=facturation.facturationNom
            Arry.append(facturationObj)
    for doctor in doctornames:
            if not any(obj['name'] == doctor.doctorname for obj in Arry):
                docObj={}
                docObj['id']=doctor.doctorid
                docObj['name']=doctor.doctorname
                Arry.append(docObj)
            

    return jsonify({'facturationnames':Arry})

@app.route('/payments',methods=['GET','POST'])
@app.route('/payments/search=<search>',methods=['GET','POST'])
@login_required
def payment(search=""):
    form=AddPaymentForm()
    export2excel_frm=Export_to_excel()
    searchform=SearchForm(searchstring=search)
    
    choices=[]
    choices.append(("---","---"))
    choices=choices+[(paytype.paiementsType,paytype.paiementsType)for paytype in db.engine.execute("select * from paymenttype").fetchall()]
    #choices.append((paytype.paiementsType,paytype.paiementsType)for paytype in db.engine.execute("select * from paymenttype").fetchall())
    
    form.paiementsType.choices = choices
    form.paiementsNom.choices= [(payname.paiementsId,payname.paiementsNom) for payname in Payment.query.filter_by(paiementsType='---').all()]
    #searchform.searchfilter.choices=[(paytype.paiementsType,paytype.paiementsType)for paytype in db.engine.execute("select * from paymenttype").fetchall()]

    payments=db.engine.execute("select * from payment where paiementsnom LIKE '%{0}%' order by paiementsId DESC".format(search))
    #payments=db.engine.execute("select * from payment  order by paiementsId DESC")
    paymentitems=payments.fetchall()
    headerspayments=payments.keys()
    payment_dataframe=pd.DataFrame(paymentitems,columns=headerspayments)
    
    if searchform.validate_on_submit() and searchform.searchsubmit.data:
        if searchform.searchstring.data !="":
            return redirect(url_for('payment',search=searchform.searchstring.data))
        else:
            return redirect(url_for('payment'))    
    else:
        print(searchform.errors)
   

    if form.is_submitted() and request.method=='POST' and form.submit.data:
        if form.paiementsNom.data!="addnew":
            new_payment =Payment(paiementsType=form.paiementsType.data,paiementsNom=form.paiementsNom.data,somme=form.somme.data,date=form.date.data,comment=form.comment.data)
        else:
            new_payment =Payment(paiementsType=form.paiementsType.data,paiementsNom=form.paiementsNomALT.data,somme=form.somme.data,date=form.date.data,comment=form.comment.data)
        if isinstance(form.somme.data, int) or isinstance(form.somme.data, float) and form.is_submitted():
            db.session.add(new_payment)
            db.session.commit()
            return redirect(url_for('payment'))
        else:
            flash("Invalid Data. Please re-check and submit again")

    if export2excel_frm.validate_on_submit() and export2excel_frm.export_submit.data:
        current_date=datetime.datetime.now()
        current_num_timestamp="{0}{1}{2}_{3}{4}{5}".format(current_date.year,current_date.month,current_date.day,current_date.hour,current_date.minute,current_date.second)
        excel_report_path=r"reporting_temporary\PAIEMENTS_{}.xlsx".format(current_num_timestamp)
        payment_dataframe.to_excel(excel_report_path,index=False)

        return send_file(excel_report_path)             
    

    
    if "payments" in current_user.access or current_user.access=="all":
        return render_template('generalform.html',forms=[form,export2excel_frm],hasDynamicSelector=True,table=paymentitems,headers=headerspayments,dbtable="payment",dbtableid="paiementsId",user_role=current_user.role,searchform=searchform)
    else:
        return render_template('NOT_AUTHORIZED.html')

@app.route('/paymentnames/<paymenttype>')
def paymentnames(paymenttype):
    paymentnames = Payment.query.filter_by(paiementsType=paymenttype).all()
    doctornames = Doctor.query.all()
    
    Arry=[]
    for payment in paymentnames:
        
        if not any(obj['name'] == payment.paiementsNom for obj in Arry):
            
            paymentObj={}
            paymentObj['id']=payment.paiementsId
            paymentObj['name']=payment.paiementsNom
            Arry.append(paymentObj)
    
    for doctor in doctornames:
            if not any(obj['name'] == doctor.doctorname for obj in Arry):
                docObj={}
                docObj['id']=doctor.doctorid
                docObj['name']=doctor.doctorname
                Arry.append(docObj)
            

    return jsonify({'paymentnames':Arry})

@app.route('/doctors',methods=['GET','POST'])
@login_required
def doctor():
    form=AddDoctorForm()
    doctors=db.engine.execute("select doctorid,doctorname,doctorspeciality,isActive,percentageShare from doctor")
    doctoritems=doctors.fetchall()
    headersdoctors=doctors.keys()
    
    if form.validate_on_submit():
        #boolean = False
        #if form.isActive.data=='True':
            #boolean = True
        new_doctor =Doctor(doctorname=form.doctorname.data,doctorspeciality=form.doctorspeciality.data,isActive=form.isActive.data,percentageShare=form.percentageShare.data,conditionsfinanciers=form.conditionsfinanciers.data)
        db.session.add(new_doctor)
        db.session.commit()
        return redirect(url_for('doctor'))
    #return render_template('doctorregisterform.html',form=form,tables=[doctors.to_html(classes='data',index=False)], titles=doctors.columns.values)
    if "doctors" in current_user.access  or current_user.access=="all":
        return render_template('doctor_setup.html',form=form,hasDynamicSelector=False,table=doctoritems,headers=headersdoctors,dbtable="doctor",dbtableid="doctorId",user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')

@app.route('/fraismateriel',methods=['GET','POST'])
@login_required
def fraismateriel():
    form =AddFraismaterielForm()
    export2excel_frm=Export_to_excel()
    fraismateriel=db.engine.execute("select * from fraismateriel")
    fraismaterielitems=fraismateriel.fetchall()
    headersfraismateriel=fraismateriel.keys()

    choices=[]
    choices.append(("---","---"))
    choices=choices+[(fraistype.fraismaterieltype,fraistype.fraismaterieltype)for fraistype in db.engine.execute("select * from fraismaterieltype").fetchall()]
    #choices.append((paytype.paiementsType,paytype.paiementsType)for paytype in db.engine.execute("select * from paymenttype").fetchall())
    
    form.fraismaterieltype.choices = choices
    form.fraismaterielnom.choices= [(fraisname.fraismaterielId,fraisname.fraismaterielnom) for fraisname in Fraismateriel.query.filter_by(fraismaterieltype='---').all()]

    if form.is_submitted() and request.method=='POST' and form.submit.data:
        if form.fraismaterielnom.data!="addnew":
            new_fraismateriel =Fraismateriel(fraismaterieltype=form.fraismaterieltype.data,fraismaterielnom=form.fraismaterielnom.data,fraismaterielsomme=form.fraismaterielsomme.data,fraismaterieldate=form.fraismaterieldate.data)
        else:
            new_fraismateriel =Fraismateriel(fraismaterieltype=form.fraismaterieltype.data,fraismaterielnom=form.fraismaterielnomALT.data,fraismaterielsomme=form.fraismaterielsomme.data,fraismaterieldate=form.fraismaterieldate.data)
        if isinstance(form.fraismaterielsomme.data, int) or isinstance(form.fraismaterielsomme.data, float) and form.is_submitted():
            db.session.add(new_fraismateriel)
            db.session.commit()
            return redirect(url_for('fraismateriel'))
        else:
            flash("Invalid Data. Please re-check and submit again")
    
    fraismaterieldf=pd.DataFrame(fraismaterielitems,columns=headersfraismateriel)
    if export2excel_frm.validate_on_submit() and export2excel_frm.export_submit.data:
        current_date=datetime.datetime.now()
        current_num_timestamp="{0}{1}{2}_{3}{4}{5}".format(current_date.year,current_date.month,current_date.day,current_date.hour,current_date.minute,current_date.second)
        excel_report_path=r"reporting_temporary\FRAIS_MATERIEL_{}.xlsx".format(current_num_timestamp)
        fraismaterieldf.to_excel(excel_report_path,index=False)

        return send_file(excel_report_path)

    if "fraismateriel" in current_user.access or current_user.access=="all":
        return render_template('generalform.html',forms=[form,export2excel_frm],hasDynamicSelector=True,table=fraismaterielitems,headers=headersfraismateriel,dbtable="fraismateriel",dbtableid="fraismaterielId",user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')


@app.route('/fraismaterielname/<fraismaterieltype>')
def fraismaterielnames(fraismaterieltype):
    fraismaterielnames = Fraismateriel.query.filter_by(fraismaterieltype=fraismaterieltype).all()
    doctornames = Doctor.query.all()
    
    Arry=[]
    for fraismateriel in fraismaterielnames:
        
        if not any(obj['name'] == fraismateriel.fraismaterielnom for obj in Arry):
            
            fraismaterielObj={}
            fraismaterielObj['id']=fraismateriel.fraismaterielId
            fraismaterielObj['name']=fraismateriel.fraismaterielnom
            Arry.append(fraismaterielObj)
    
    for doctor in doctornames:
            if not any(obj['name'] == doctor.doctorname for obj in Arry):
                docObj={}
                docObj['id']=doctor.doctorid
                docObj['name']=doctor.doctorname
                Arry.append(docObj)
            

    return jsonify({'fraismaterielnames':Arry})




@app.route('/load_doctor/tbl=<tbl>/id=<id>',methods=['GET','POST'])
@login_required
def load_doctor(tbl,id):
    if tbl=='doctor':
        qry = Doctor.query.filter(
            Doctor.doctorid==id).first()
        #doc = qry.first()
        
        form=AddDoctorConstantsForm(obj=qry)
        #subform=AddDoctorConstantsForm(obj=qry)

        leasing_form=LeasingForm()
        leasingdata=db.engine.execute("select LeasingId,LocationNom,debut,finPrevue,paiement from leasing where docteur='{0}'".format(qry.doctorname))
        leasingdataitems=leasingdata.fetchall()
        headersleasingdata=leasingdata.keys()

        if leasing_form.validate_on_submit() and request.method=='POST' and leasing_form.leasesubmit.data:
            new_leasing=Leasing(locationNom=leasing_form.locationNom.data,docteur=qry.doctorname,debut=leasing_form.debut.data,finPrevue=leasing_form.finPrevue.data,paiement=leasing_form.paiement.data)
            db.session.add(new_leasing)
            db.session.commit()
            return redirect(request.url)

        if form.is_submitted() and request.method=='POST' and form.submit.data:
            #qry.doctorid = form.doctorid.data
            qry.doctorname=form.doctorname.data
            qry.isActive = form.isActive.data
            qry.doctorspeciality=form.doctorspeciality.data
            qry.percentageShare=form.percentageShare.data
            qry.conditionsfinanciers=form.conditionsfinanciers.data
            #print(subform.surfacecentremedical.value)
            qry.surfacecentremedical=form.surfacecentremedical.data
            qry.surfacecommunes=form.surfacecommunes.data
            qry.loyermensuel=form.loyermensuel.data
            qry.surfaceaccordee=form.surfaceaccordee.data
            qry.nettoyage=form.nettoyage.data
            qry.conciergerie=form.conciergerie.data
            qry.salairepersonnel=form.salairepersonnel.data
            qry.telephonieinternet=form.telephonieinternet.data
            qry.logicielaxenita=form.logicielaxenita.data
            qry.nbmedicins=form.nbmedicins.data
            qry.assurances=form.assurances.data
            qry.blanchisserieleman=form.blanchisserieleman.data
            qry.informatique=form.informatique.data
            qry.nblocaux=form.nblocaux.data
            qry.nbmedicinsrepartirfrais=form.nbmedicinsrepartirfrais.data
            qry.receptionniste=form.receptionniste.data
            qry.Apprentie=form.Apprentie.data
            
            #qry=form
            db.session.commit()
            return redirect(url_for('doctor'))    
        else:
            print(form.errors)
    return render_template('edit_doctor.html',form=form,leasingform=leasing_form,headers=headersleasingdata,table=leasingdataitems,user_role=current_user.role,dbtable="leasing",dbtableid="leasingId")


@app.route('/edit_entry/tbl=<tbl>/id=<id>',methods=['GET','POST'])
@login_required
def edit_entry(tbl,id):

    if tbl=='fraismateriel':
        qry=Fraismateriel.query.filter(
            Fraismateriel.fraismaterielId==id
        ).first()



        form=AddFraismaterielForm(obj=qry)
        choices=[]
        choices.append(("---","---"))
        choices=choices+[(fraistype.fraismaterieltype,fraistype.fraismaterieltype)for fraistype in db.engine.execute("select * from fraismaterieltype").fetchall()]
        #choices.append((paytype.paiementsType,paytype.paiementsType)for paytype in db.engine.execute("select * from paymenttype").fetchall())
    
        form.fraismaterieltype.choices = choices
        

        form.fraismaterielnom.choices=[(qry.fraismaterielnom,qry.fraismaterielnom)]

        if form.validate_on_submit():
            #qry.doctorid = form.doctorid.data
            qry.fraismaterieltype=form.fraismaterieltype.data
            if form.fraismaterielnomALT.data=="":
                qry.fraismaterielnom = form.fraismaterielnom.data
            else:
                qry.fraismaterielnom = form.fraismaterielnomALT.data
            qry.fraismaterielsomme=form.fraismaterielsomme.data
            qry.fraismaterieldate=form.fraismaterieldate.data
            #qry.comment=form.comment.data
            if isinstance(form.fraismaterielsomme.data, int) or isinstance(form.fraismaterielsomme.data, float) and form.is_submitted():
            #qry=form

                db.session.commit()
            else:
                flash("Invalid Data. Please re-check and submit again") 
            return redirect(url_for('fraismateriel'))
       

    if tbl=='doctorpayment':
        qry = Doctorpayment.query.filter(
            Doctorpayment.doctorpaiementId==id
        ).first()

        form=AddDoctorPaymentForm(obj=qry)

        choices=[]
        #choices.append(("---","---"))
        choices=choices+[(doctor.doctorname,doctor.doctorname)for doctor in db.engine.execute("select doctorname from doctor").fetchall()]   
        form.doctorname.choices=choices
        
        paymentchoices=[]
        paymentchoices.append(("addnew","Ajouter Nouveau ?"))
        paymentchoices=paymentchoices+[(doctor.paimentnom,doctor.paimentnom)for doctor in db.engine.execute("select DISTINCT paimentnom   from doctorpayment").fetchall()]
        form.paimentnom.choices=paymentchoices
        #form.paimentnom.data=qry.paimentnom 
        

        if form.validate_on_submit():
            #qry.doctorid = form.doctorid.data
            qry.doctorname=form.doctorname.data
            if form.paimentnom.data=="addnew":
                qry.paimentnom=form.paimentnomALT.data
            else:    
                qry.paimentnom=form.paimentnom.data
            qry.doctorpaiementsomme=form.doctorpaiementsomme.data
            
            #qry=form
            db.session.commit()
            return redirect(url_for('doctorpayment'))               

    
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
            qry.comment=form.comment.data
            
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
            qry.comment=form.comment.data
            
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
    if tbl=="encaissement":
        qry=Encaissement.query.filter(Encaissement.encaissementId==id).first()
        form=AddEncaissementForm(obj=qry)
        encaissementnameschoices = []
        encaissementnameschoices.append(("addnew","Ajouter Nouveau ?"))
        for encname in db.engine.execute("select * from encaissement").fetchall():
            if not any(obj[0] == encname.encaissementNom for obj in encaissementnameschoices):
                encaissementnameschoices.append((encname.encaissementNom,encname.encaissementNom))

        form.encaissementNom.choices = encaissementnameschoices
        if form.validate_on_submit():
            qry.encaissementDate=form.encaissementDate.data
            
            if form.encaissementNom.data!="addnew":
                qry.encaissementNom=form.encaissementNom.data
            else:   
                qry.encaissementNom=form.encaissementNomALT.data 
            qry.montant=form.montant.data
            qry.banque=form.banque.data
            qry.comment=form.comment.data
            db.session.commit()
            return redirect(url_for('encaissement'))

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
        

    return render_template('edititem.html',form=form,tbl=tbl)



@app.route('/delete_entry/tbl=<tbl>/tblid=<tblid>/id=<id>',methods=['GET','POST'])
@login_required
def delete_entry(tbl,tblid,id):
    db.engine.execute("delete from \"{0}\" where {1}={2}".format(tbl,tblid,id))
    db.session.commit()
    if 'type' in tbl:
        return redirect(url_for('setup'))
    elif 'leasing' in tbl:
        return redirect(url_for('load_doctor',tbl=tbl,id=id))
    else:
        return redirect(url_for(tbl))



@app.route('/user',methods=['GET','POST'])
def user():
    form=RegisterForm()
    userlslist=db.engine.execute("select id,username,role,access from \"user\"")
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
        return render_template("user.html",form=form,table=userlslistitems,headers=headersuserlslist,username=current_user.username,user_role=current_user.role,dbtable="user",dbtableid="id")
    else:
        return render_template("NOT_AUTHORIZED.html")

def convert_list_to_dataframe(input_list):
    items=input_list.fetchall()
    headers=input_list.keys()
    output_dataframe = pd.DataFrame(items,columns=headers)

    return output_dataframe

def fetch_doctor_info(doctorname):
    qry = Doctor.query.filter(
            Doctor.doctorname==doctorname
        ).first()
    try:
        nbmedicinsrepartirfrais=getattr(qry,"nbmedicinsrepartirfrais")
        informatique=getattr(qry,"informatique")
        assurances=getattr(qry,"assurances")

        dict_to_return={
            "informatique":informatique if informatique != 0 and informatique is not None else 0.1 ,
            "nbmedicinsrepartirfrais":nbmedicinsrepartirfrais if nbmedicinsrepartirfrais != 0 and nbmedicinsrepartirfrais is not None else 0.1 ,
            "assurances":assurances if assurances != 0 and assurances is not None else 0.1 
        }
        
        return dict_to_return
    except:
        return None

@app.route('/reporting',methods=['GET','POST'])
@login_required
def reporting():

    #print(paymentdf)
    form=MainReportForm()
    ind_doctor_form=IndividualDoctorReportForm()
    choices=[]
    #choices.append(("---","---"))
    choices=choices+[(doctor.doctorname,doctor.doctorname)for doctor in db.engine.execute("select doctorname from doctor").fetchall()]   
    ind_doctor_form.doctorname.choices=choices


    if ind_doctor_form.validate_on_submit():
        current_date=datetime.datetime.now()
        current_num_timestamp="{0}{1}{2}_{3}{4}{5}".format(current_date.year,current_date.month,current_date.day,current_date.hour,current_date.minute,current_date.second)
        doctor_report_filename=r'reporting_temporary\RAPPORT_MEDECINS_{0}.pdf'.format(current_num_timestamp)
        dfs=[]

        varying_paymentslist=db.engine.execute("""select paimentnom AS PaiementNom,doctorpaiementsomme AS Somme,date AS Date FROM doctorpayment where doctorname='{0}' and YEAR(date)={1}""".format(ind_doctor_form.doctorname.data,ind_doctor_form.year.data))
        varying_paymentsdf=convert_list_to_dataframe(varying_paymentslist)
        varying_paymentsdf.set_index("PaiementNom",inplace=True)

        dfs.append((varying_paymentsdf.fillna(0).round(2),"Paeiment Medcins"))

        composite_df = pd.DataFrame(columns=['Charges','Cout Mensuel','Cout Annuel'])
        
        composite_df.set_index('Charges',inplace=True)
        #print(composite_df)
        dataa=fetch_doctor_info(ind_doctor_form.doctorname.data)

        informatique_ann=dataa["informatique"]/dataa["nbmedicinsrepartirfrais"]
        informatique_men=informatique_ann/12

        assurance_ann=dataa["assurances"]/dataa["nbmedicinsrepartirfrais"]
        assurance_men=assurance_ann/12

        temp_df2 = pd.DataFrame({
                    "Cout Mensuel": [informatique_men,assurance_men],
                    "Cout Annuel":[informatique_ann,assurance_ann]},
                   index=["Informatique","Assurances"])

        composite_df=pd.concat([composite_df, temp_df2])
        #print(composite_df)

        dfs.append((composite_df.fillna(0).round(2),"Charges Mensuel/Annuel"))

        leasinglist=db.engine.execute("""Select locationNom as LocationNom,
debut as Debut,
finPrevue as FinPrevue,
paiement as PaiementMensuel,
paiement*12 as PaiementAnnuel
From leasing
where docteur='{0}'""".format(ind_doctor_form.doctorname.data))
        leasingdf=convert_list_to_dataframe(leasinglist)
        leasingdf.set_index("LocationNom",inplace=True)

        dfs.append((leasingdf.fillna(0).round(2),"Locations(Leasing)"))


        doctor_report(dfs,ind_doctor_form.doctorname.data,ind_doctor_form.year.data,doctor_report_filename)

        

        return send_file(doctor_report_filename)









    if form.validate_on_submit():
        dfs=[]
        #paymentslist=db.engine.execute("""SELECT paiementsNom,SUM(somme) AS somme FROM payment GROUP BY paiementsNom;""")
        paymentslist=db.engine.execute("""select paiementsType, SUM(somme) AS somme ,MONTH(date) AS "month" From payment where YEAR(date)={0} group by YEAR(date),MONTH(date) , paiementsType """.format(form.year.data))

        paymentdf=convert_list_to_dataframe(paymentslist)
        paymentdf.set_index('paiementsType',inplace=True)

        paymentforgraphlist=db.engine.execute("""select paiementsType, SUM(somme) AS somme ,YEAR(date) as "year" From payment where YEAR(date)=2022 group by YEAR(date) , paiementsType""".format(form.year.data))
        paymentforgraphdf=convert_list_to_dataframe(paymentforgraphlist)
        paymentforgraphdf.set_index('paiementsType',inplace=True)

        paymentforreportlist=db.engine.execute("""SELECT paiementsType AS PaiementType, 
	SUM (CASE WHEN Month(date)=1 THEN somme END) AS January,
	SUM (CASE WHEN Month(date)=2 THEN somme END) AS February,
	SUM (CASE WHEN Month(date)=3 THEN somme END) AS March,
	SUM (CASE WHEN Month(date)=4 THEN somme END) AS April,
	SUM (CASE WHEN Month(date)=5 THEN somme END) AS May,
	SUM (CASE WHEN Month(date)=6 THEN somme END) AS June,
	SUM (CASE WHEN Month(date)=7 THEN somme END) AS July,
	SUM (CASE WHEN Month(date)=8 THEN somme END) AS August,
	SUM (CASE WHEN Month(date)=9 THEN somme END) AS September,
	SUM (CASE WHEN Month(date)=10 THEN somme END) AS October,
	SUM (CASE WHEN Month(date)=11 THEN somme END) AS November,
	SUM (CASE WHEN Month(date)=12 THEN somme END) AS December

FROM payment
WHERE Year(date)={0}
GROUP BY paiementsType""".format(form.year.data))
        paymentforreportdf=convert_list_to_dataframe(paymentforreportlist)
        paymentforreportdf.set_index('PaiementType',inplace=True)        


        dfs.append((paymentforreportdf.fillna(0).round(2),paymentforgraphdf.fillna(0).round(2),"Paiements tout au long de l'année"))


        encaissementlist=db.engine.execute("""select encaissementNom,SUM(montant) AS somme,banque from encaissement where YEAR(encaissementDate)={0} group by encaissementNom,banque""".format(form.year.data))
        encaissementdf=convert_list_to_dataframe(encaissementlist)
        encaissementdf.rename(columns = {'montant':'somme'}, inplace = True)
        encaissementdf.set_index('encaissementNom',inplace=True)
        #print(encaissementdf)

        encaissementgraphlist=db.engine.execute("""select SUM(montant) AS somme,banque from encaissement where YEAR(encaissementDate)={0} group by banque""".format(form.year.data))
        encaissementgraphdf=convert_list_to_dataframe(encaissementgraphlist)
        encaissementgraphdf.set_index('banque',inplace=True)
        
        dfs.append((encaissementdf.fillna(0).round(2),encaissementgraphdf.fillna(0).round(2),"Encaissement"))

        '''facturationlist = db.engine.execute("""select facturationType, SUM(somme) AS somme ,MONTH(date) AS "month",YEAR(date) as "year" From facturation where YEAR(date)={0} group by YEAR(date),MONTH(date) , facturationType""".format(form.year.data))
        
        facturationdf=convert_list_to_dataframe(facturationlist)
        facturationdf.set_index('facturationType',inplace=True)'''
        facturationgraphlist=db.engine.execute("""select facturationType, SUM(somme) AS somme ,YEAR(date) as "year" From facturation where YEAR(date)={0} group by YEAR(date) , facturationType""".format(form.year.data))
        facturationgraphdf=convert_list_to_dataframe(facturationgraphlist)
        facturationgraphdf.set_index('facturationType',inplace=True)

        facturationforreportlist=db.engine.execute("""SELECT facturationType AS FacturationType, 
	SUM (CASE WHEN Month(date)=1 THEN somme END) AS January,
	SUM (CASE WHEN Month(date)=2 THEN somme END) AS February,
	SUM (CASE WHEN Month(date)=3 THEN somme END) AS March,
	SUM (CASE WHEN Month(date)=4 THEN somme END) AS April,
	SUM (CASE WHEN Month(date)=5 THEN somme END) AS May,
	SUM (CASE WHEN Month(date)=6 THEN somme END) AS June,
	SUM (CASE WHEN Month(date)=7 THEN somme END) AS July,
	SUM (CASE WHEN Month(date)=8 THEN somme END) AS August,
	SUM (CASE WHEN Month(date)=9 THEN somme END) AS September,
	SUM (CASE WHEN Month(date)=10 THEN somme END) AS October,
	SUM (CASE WHEN Month(date)=11 THEN somme END) AS November,
	SUM (CASE WHEN Month(date)=12 THEN somme END) AS December

FROM facturation
WHERE Year(date)={0}
GROUP BY facturationType""".format(form.year.data))
        facturationforreportdf=convert_list_to_dataframe(facturationforreportlist)
        facturationforreportdf.set_index('FacturationType',inplace=True) 

        dfs.append((facturationforreportdf.fillna(0).round(2),facturationgraphdf.fillna(0).round(2),"Facturation"))


        #print(encaissementdf.sum()["montant"])
        enctotal=encaissementdf.sum()["somme"]
        #print(paymentdf.sum()["somme"])
        paymenttotal=paymentdf.sum()["somme"]

        #print(enctotal-paymenttotal)
        pnl=enctotal-paymenttotal

        
        current_date=datetime.datetime.now()

        current_num_timestamp="{0}{1}{2}_{3}{4}{5}".format(current_date.year,current_date.month,current_date.day,current_date.hour,current_date.minute,current_date.second)
        report_filename=r'reporting_temporary\RAPPORT_{0}.pdf'.format(current_num_timestamp)
        
        dataframe_to_pdf(dfs,pnl,form.year.data,report_filename,enctotal,paymenttotal)        

        return send_file(report_filename)






    if "reports" in current_user.access  or current_user.access=="all":
        
        return render_template("reporting.html",forms=[form,ind_doctor_form],formtitles=["Rapport Général (P&L)","Rapport du Médecin"])
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

    form4 = AddFraismaterieltype()
    fraismaterieltypes=db.engine.execute("select * from Fraismaterieltype")
    fraismaterielitems=fraismaterieltypes.fetchall()
    headersfraismaterieltypes=fraismaterieltypes.keys()

    if form4.validate_on_submit():
        new_fraismateriel_type=Fraismaterieltype(fraismaterieltype=form4.fraismaterieltype.data)
        db.session.add(new_fraismateriel_type)
        db.session.commit()
        return redirect(url_for('setup'))


    if "setup" in current_user.access  or current_user.access=="all":        
        return render_template('setup.html',forms=[form1,form2,form3,form4],table=[paymenttypesitems,facturationtypesitems,dentisterietypesitems,fraismaterielitems],headers=[headerspaymenttypes,headersfacturationtypes,headersdentisterietypes,headersfraismaterieltypes],dbtable=["paymenttype","facturationtype","dentisterietype","fraismaterieltype"],dbtableid=["paiementstypeid","facturationtypeid","dentisterietypeid","fraismaterieltypeid"],titles=["Paiement Types","Facturation Types","Dentisterie Types","Frais Materiel Types"],user_role=current_user.role)
    else:
        return render_template('NOT_AUTHORIZED.html')



@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0")