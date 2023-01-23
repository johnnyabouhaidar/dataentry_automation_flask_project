from DB_layer import *
from flask import Flask, render_template, url_for,redirect, flash,send_file, jsonify,request,session
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

file_download_location= r"C:\Users\Public\Documents"

db=SQLAlchemy(app)
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

    pourcentagesalaire=db.Column(db.Float)
    pourcentagechargessociales=db.Column(db.Float)
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
    simplify=db.Column(db.Float)
    steriswiss=db.Column(db.Float)


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
    comment=db.Column(db.String(250))

class Leasing(db.Model):
    LeasingId=db.Column(db.Integer,primary_key=True)
    locationNom=db.Column(db.String(80),nullable=False)
    docteur=db.Column(db.String(80),nullable=False)
    debut=db.Column(db.Date,nullable=False)
    finPrevue=db.Column(db.Date,nullable=False)
    paiement=db.Column(db.Float,nullable=True)
    paiementinitial=db.Column(db.Float,nullable=True)

class Percentageactivity(db.Model):
    activiteId=db.Column(db.Integer,primary_key=True)
    docteur=db.Column(db.String(80),nullable=False)
    de=db.Column(db.Integer,nullable=False)
    a=db.Column(db.Integer,nullable=False)
    pourcentages=db.Column(db.Float,nullable=False)




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





def get_ls_for_dashboard(query):
    encaissementgraphlist=db.engine.execute(query)
    encaissementgraphdf=convert_list_to_dataframe(encaissementgraphlist)
    encaissementgraphdf=encaissementgraphdf.round(2)
    ls=encaissementgraphdf.values.tolist()
    ls.insert(0,encaissementgraphdf.columns.tolist())
    total = encaissementgraphdf["somme"].sum()
    #total = '{:0,.2f}'.format(total)

    return ls,total


@app.route('/dashboard',methods=['GET','POST'])
#@app.route('/dashboard/usr=<usr>',methods=['GET','POST'])
@login_required
def dashboard():
    encls,enctotal = get_ls_for_dashboard("""select banque, SUM(montant) AS somme from encaissement where YEAR(encaissementDate)={0} group by banque""".format(2022))
    paymentls,paysum = get_ls_for_dashboard("""Select paiementstype as PaiementType, SUM(somme)  as somme from payment group by paiementsType """)
    facturationls,facturationsum = get_ls_for_dashboard("""Select facturationtype as FacturationType, SUM(somme)  as somme from facturation group by facturationType""")
    pnl=enctotal-paysum
    paysum = '{:0,.2f}'.format(paysum)
    pnl= '{:0,.2f}'.format(pnl)
    facturationsum='{:0,.2f}'.format(facturationsum)

    return render_template('dashboard.html',username=(current_user.username).title(),user_role=current_user.role,encdf=encls,paymentgrph=paymentls,paysum=paysum,pnl=pnl,facturationsum=facturationsum)


@app.route('/doctorpayment',methods=['GET','POST'])
@app.route('/doctorpayment/search=<search>',methods=['GET','POST'])
@login_required
def doctorpayment(search=""):
    form=AddDoctorPaymentForm()
    searchform=SearchForm(searchstring=search)
    choices=[]
    #choices.append(("---","---"))
    choices=choices+[(doctor.doctorname,doctor.doctorname)for doctor in db.engine.execute("select doctorname from doctor").fetchall()]   
    form.doctorname.choices=choices

    paymentchoices=[]
    paymentchoices.append(("addnew","Ajouter Nouveau ?"))
    paymentchoices=paymentchoices+[(doctorpay.paimentnom,doctorpay.paimentnom)for doctorpay in db.engine.execute("select DISTINCT paimentnom   from doctorpayment").fetchall()]
    form.paimentnom.choices=paymentchoices


    DoctorPayments=db.engine.execute("select * from DoctorPayment where paimentnom LIKE '%{0}%' order by doctorpaiementId DESC".format(search))
    DoctorPaymentitems=DoctorPayments.fetchall()
    headersDoctorPayment=DoctorPayments.keys()

    if searchform.validate_on_submit() and searchform.searchsubmit.data:
        if searchform.searchstring.data !="":
            return redirect(url_for('doctorpayment',search=searchform.searchstring.data))
        else:
            return redirect(url_for('doctorpayment'))    
    else:
        print(searchform.errors)

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
        return render_template('generalform.html',forms=[form],hasDynamicSelector=False,table=DoctorPaymentitems,headers=headersDoctorPayment,dbtable="doctorpayment",dbtableid="doctorpaiementId",user_role=current_user.role,searchform=searchform,module_name="Paiement Docteur")
    else:
        return render_template('NOT_AUTHORIZED.html')

@app.route('/encaissement',methods=['GET','POST'])
@app.route('/encaissement/search=<search>',methods=['GET','POST'])
@login_required
def encaissement(search=""):
    form = AddEncaissementForm()
    export2excel_frm=Export_to_excel()
    searchform=SearchForm(searchstring=search)
    encaissementnameschoices = []
    encaissementnameschoices.append(("addnew","Ajouter Nouveau ?"))
    for encname in db.engine.execute("select * from encaissement").fetchall():
        if not any(obj[0] == encname.encaissementNom for obj in encaissementnameschoices):
            encaissementnameschoices.append((encname.encaissementNom,encname.encaissementNom))

    form.encaissementNom.choices = encaissementnameschoices
    encaissements=db.engine.execute("select * from encaissement where encaissementNom LIKE '%{0}%'  order by encaissementId DESC".format(search))
    encaissementitems=encaissements.fetchall()
    headersencaissement=encaissements.keys()

    if searchform.validate_on_submit() and searchform.searchsubmit.data:
        if searchform.searchstring.data !="":
            return redirect(url_for('encaissement',search=searchform.searchstring.data))
        else:
            return redirect(url_for('encaissement'))    
    else:
        print(searchform.errors)

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
        excel_report_path=r"{0}\reporting_temporary\ENCAISSEMENT_{1}.xlsx".format(file_download_location,current_num_timestamp)
        encaissementdf.to_excel(excel_report_path,index=False)

        return send_file(excel_report_path)

    if "encaissement" in current_user.access or current_user.access=="all":
        return render_template('generalform.html',forms=[form],hasDynamicSelector=True,table=encaissementitems,headers=headersencaissement,dbtable="encaissement",dbtableid="encaissementId",user_role=current_user.role,searchform=searchform,module_name="Encaissement-Avance",export_form=export2excel_frm)
    else:
        return render_template('NOT_AUTHORIZED.html')


@app.route('/dentisterie',methods=['GET','POST'])
@app.route('/dentisterie/search=<search>',methods=['GET','POST'])
@login_required
def dentisterie(search=""):
    form=AddDentistryInfoForm()
    searchform=SearchForm(searchstring=search)
    choices=[]
    choices.append(("---","---"))
    choices=choices+[(denttype.dentisterietype,denttype.dentisterietype)for denttype in db.engine.execute("select * from dentisterietype").fetchall()]   
    form.dentisterieType.choices=choices
    form.dentisterieNom.choices= [(dentname.dentisterieId,dentname.dentisterieNom) for dentname in Dentisterie.query.filter_by(dentisterieType='---').all()]
    dentisterie=db.engine.execute("select * from dentisterie where dentisterieNom LIKE '%{0}%'  order by dentisterieId DESC".format(search))
    dentisterieitems=dentisterie.fetchall()
    headersdentisterie=dentisterie.keys()

    if searchform.validate_on_submit() and searchform.searchsubmit.data:
        if searchform.searchstring.data !="":
            return redirect(url_for('dentisterie',search=searchform.searchstring.data))
        else:
            return redirect(url_for('dentisterie'))    
    else:
        print(searchform.errors)

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
        return render_template('generalform.html',forms=[form],hasDynamicSelector=True,table=dentisterieitems,headers=headersdentisterie,dbtable="dentisterie",dbtableid="dentisterieId",user_role=current_user.role,searchform=searchform,module_name="Dentisterie")
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
@app.route('/facturation/search=<search>',methods=['GET','POST'])
@login_required
def facturation(search=""):
    form = AddFacturationForm()
    export2excel_frm=Export_to_excel()
    searchform=SearchForm(searchstring=search)
    choices=[]
    choices.append(("---","---"))
    choices=choices+[(facttype.facturationType,facttype.facturationType)for facttype in db.engine.execute("select * from facturationtype").fetchall()]
    form.facturationType.choices = choices
    form.facturationNom.choices= [(factname.facturationId,factname.facturationNom) for factname in Facturation.query.filter_by(facturationType='---').all()]
    facturations=db.engine.execute("select * from facturation where facturationnom LIKE '%{0}%' order by facturationId DESC".format(search))
    facturationsitems=facturations.fetchall()
    headersfacturations=facturations.keys()

    facturationdf=pd.DataFrame(facturationsitems,columns=headersfacturations)
    if export2excel_frm.validate_on_submit() and export2excel_frm.export_submit.data:
        current_date=datetime.datetime.now()
        current_num_timestamp="{0}{1}{2}_{3}{4}{5}".format(current_date.year,current_date.month,current_date.day,current_date.hour,current_date.minute,current_date.second)
        excel_report_path=r"{0}\reporting_temporary\FACTURATION_{1}.xlsx".format(file_download_location,current_num_timestamp)
        facturationdf.to_excel(excel_report_path,index=False)

        return send_file(excel_report_path)

    if searchform.validate_on_submit() and searchform.searchsubmit.data:
        if searchform.searchstring.data !="":
            return redirect(url_for('facturation',search=searchform.searchstring.data))
        else:
            return redirect(url_for('facturation'))    
    else:
        print(searchform.errors)

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
        return render_template('generalform.html',forms=[form],hasDynamicSelector=True,table=facturationsitems,headers=headersfacturations,dbtable="facturation",dbtableid="facturationId",user_role=current_user.role,searchform=searchform,module_name="Facturation",export_form=export2excel_frm)
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
        excel_report_path=r"{0}\reporting_temporary\PAIEMENTS_{1}.xlsx".format(file_download_location,current_num_timestamp)
        payment_dataframe.to_excel(excel_report_path,index=False)

        return send_file(excel_report_path)             
    

    
    if "payments" in current_user.access or current_user.access=="all":
        return render_template('generalform.html',forms=[form],hasDynamicSelector=True,table=paymentitems,headers=headerspayments,dbtable="payment",dbtableid="paiementsId",user_role=current_user.role,searchform=searchform,module_name="Paiement",export_form=export2excel_frm)
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
@app.route('/fraismateriel/search=<search>',methods=['GET','POST'])
@login_required
def fraismateriel(search=""):
    form =AddFraismaterielForm()
    export2excel_frm=Export_to_excel()
    searchform=SearchForm(searchstring=search)
    fraismateriel=db.engine.execute("select * from fraismateriel where fraismaterielnom LIKE '%{0}%' order by fraismaterielId DESC".format(search))
    fraismaterielitems=fraismateriel.fetchall()
    headersfraismateriel=fraismateriel.keys()

    choices=[]
    choices.append(("---","---"))
    choices=choices+[(fraistype.fraismaterieltype,fraistype.fraismaterieltype)for fraistype in db.engine.execute("select * from fraismaterieltype").fetchall()]
    #choices.append((paytype.paiementsType,paytype.paiementsType)for paytype in db.engine.execute("select * from paymenttype").fetchall())
    
    form.fraismaterieltype.choices = choices
    form.fraismaterielnom.choices= [(fraisname.fraismaterielId,fraisname.fraismaterielnom) for fraisname in Fraismateriel.query.filter_by(fraismaterieltype='---').all()]

    if searchform.validate_on_submit() and searchform.searchsubmit.data:
        if searchform.searchstring.data !="":
            return redirect(url_for('fraismateriel',search=searchform.searchstring.data))
        else:
            return redirect(url_for('fraismateriel'))    
    else:
        print(searchform.errors)

    if form.is_submitted() and request.method=='POST' and form.submit.data:
        if form.fraismaterielnom.data!="addnew":
            new_fraismateriel =Fraismateriel(fraismaterieltype=form.fraismaterieltype.data,fraismaterielnom=form.fraismaterielnom.data,fraismaterielsomme=form.fraismaterielsomme.data,fraismaterieldate=form.fraismaterieldate.data,comment=form.comment.data)
        else:
            new_fraismateriel =Fraismateriel(fraismaterieltype=form.fraismaterieltype.data,fraismaterielnom=form.fraismaterielnomALT.data,fraismaterielsomme=form.fraismaterielsomme.data,fraismaterieldate=form.fraismaterieldate.data,comment=form.comment.data)
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
        excel_report_path=r"{0}\reporting_temporary\FRAIS_MATERIEL_{1}.xlsx".format(file_download_location,current_num_timestamp)
        fraismaterieldf.to_excel(excel_report_path,index=False)

        return send_file(excel_report_path)

    if "fraismateriel" in current_user.access or current_user.access=="all":
        return render_template('generalform.html',forms=[form],hasDynamicSelector=True,table=fraismaterielitems,headers=headersfraismateriel,dbtable="fraismateriel",dbtableid="fraismaterielId",user_role=current_user.role,searchform=searchform,module_name="Frais Materiel",export_form=export2excel_frm)
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
        session['curr_route']=request.path
        qry = Doctor.query.filter(
            Doctor.doctorid==id).first()
        #doc = qry.first()
        
        form=AddDoctorConstantsForm(obj=qry)
        #subform=AddDoctorConstantsForm(obj=qry)

        leasing_form=LeasingForm()
        leasingdata=db.engine.execute("select LeasingId,LocationNom,debut,finPrevue,paiement,paiementinitial from leasing where docteur='{0}'".format(qry.doctorname))
        leasingdataitems=leasingdata.fetchall()
        headersleasingdata=leasingdata.keys()

        if leasing_form.validate_on_submit() and request.method=='POST' and leasing_form.leasesubmit.data:
            new_leasing=Leasing(locationNom=leasing_form.locationNom.data,docteur=qry.doctorname,debut=leasing_form.debut.data,finPrevue=leasing_form.finPrevue.data,paiement=leasing_form.paiement.data,paiementinitial=leasing_form.paiementinitial.data)
            db.session.add(new_leasing)
            db.session.commit()
            return redirect(request.url)

        perc_act_form=PercentageactivityForm()
        perc_act_data=db.engine.execute("select activiteId,de,a,pourcentages from percentageactivity where docteur='{0}'".format(qry.doctorname))
        perc_act_dataitems=perc_act_data.fetchall()
        headersperc_act_data=perc_act_data.keys()

        if perc_act_form.validate_on_submit() and request.method=='POST' and perc_act_form.submit.data:
            new_perc_act=Percentageactivity(de=perc_act_form.de.data,docteur=qry.doctorname,a=perc_act_form.a.data,pourcentages=perc_act_form.pourcentages.data)
            db.session.add(new_perc_act)
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

            qry.pourcentagesalaire=form.pourcentagesalaire.data
            qry.pourcentagechargessociales=form.pourcentagechargessociales.data
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
            qry.simplify=form.simplify.data
            qry.steriswiss=form.steriswiss.data
            
            #qry=form
            db.session.commit()
            return redirect(url_for('doctor'))    
        else:
            print(form.errors)
    return render_template('edit_doctor.html',form=form,leasingform=leasing_form,perc_act_form=perc_act_form,headers=headersleasingdata,table=leasingdataitems,headersperc_act_data=headersperc_act_data,perc_act_dataitems=perc_act_dataitems,user_role=current_user.role,dbtable="leasing",dbtableid="leasingId",perc_act_dbtable="percentageactivity",perc_act_id="activiteId")


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

        if form.validate_on_submit()  :
            #qry.doctorid = form.doctorid.data
            qry.fraismaterieltype=form.fraismaterieltype.data
            if form.fraismaterielnomALT.data=="":
                qry.fraismaterielnom = form.fraismaterielnom.data
            else:
                qry.fraismaterielnom = form.fraismaterielnomALT.data
            qry.fraismaterielsomme=form.fraismaterielsomme.data
            qry.fraismaterieldate=form.fraismaterieldate.data
            qry.comment=form.comment.data
            #qry.comment=form.comment.data
            if isinstance(form.fraismaterielsomme.data, int) or isinstance(form.fraismaterielsomme.data, float):
            #qry=form   

                db.session.commit()
                return redirect(url_for('fraismateriel'))
        elif form.is_submitted():
            flash("Invalid Data. Please re-check and submit again") 
            
       

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
        elif form.is_submitted():
            flash("Invalid Data. Please re-check and submit again!")
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
        elif form.is_submitted():
            flash("Invalid Data. Please re-check and submit again!")
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
        elif form.is_submitted():
            flash("Invalid Data. Please re-check and submit again!")
    if tbl=="encaissement":
        qry=Encaissement.query.filter(Encaissement.encaissementId==id).first()
        form=AddEncaissementForm(obj=qry,banque=qry.banque.strip())
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
        elif form.is_submitted():
            flash("Invalid Data. Please re-check and submit again!")

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
        current_route=session.get('curr_route',None)
        return redirect(current_route)
    elif 'percentageactivity' in tbl:
        current_route=session.get('curr_route',None)
        return redirect(current_route)
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
        return redirect(url_for('user'))
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
        blanchisserie=getattr(qry,"blanchisserieleman")
        nbmedicins=getattr(qry,"nbmedicins")
        logicielaxenita=getattr(qry,"logicielaxenita")
        telephonieinternet=getattr(qry,"telephonieinternet")
        simplify=getattr(qry,"simplify")
        conciergerie=getattr(qry,"conciergerie")
        nettoyage=getattr(qry,"nettoyage")
        surfaceaccordee=getattr(qry,"surfaceaccordee")
        surfacecentremedical=getattr(qry,"surfacecentremedical")
        loyermensuel=getattr(qry,"loyermensuel")
        surfacecommunes=getattr(qry,"surfacecommunes")
        pourcentagesalaire=getattr(qry,"pourcentagesalaire")
        pourcentagechargessociales=getattr(qry,"pourcentagechargessociales")
        salairepersonnel=getattr(qry,"salairepersonnel")
        #pourcentagechargessociales=getattr(qry,"pourcentagechargessociales")
        surfaceaccordee=getattr(qry,"surfaceaccordee")


        dict_to_return={
            "informatique":informatique if informatique != 0 and informatique is not None else 0.1 ,
            "nbmedicinsrepartirfrais":nbmedicinsrepartirfrais if nbmedicinsrepartirfrais != 0 and nbmedicinsrepartirfrais is not None else 0.1 ,
            "assurances":assurances if assurances != 0 and assurances is not None else 0.1, 
            "blanchisserie":blanchisserie if blanchisserie!=0 and blanchisserie is not None else 0.1,
            "nbmedicins":nbmedicins if nbmedicins!=0 and nbmedicins is not None else 0.1,
            "logicielaxenita":logicielaxenita if logicielaxenita!=0 and logicielaxenita is not None else 0.1,
            "telephonieinternet":telephonieinternet if telephonieinternet !=0 and telephonieinternet is not None else 0.1,
            "simplify":simplify if simplify !=0 and simplify is not None else 0.1,
            "conciergerie":conciergerie if conciergerie!=0 and conciergerie is not None else 0.1,
            "nettoyage":nettoyage if nettoyage!=0 and nettoyage is not None else 0.1,
            "surfaceaccordee":surfaceaccordee if surfaceaccordee!=0 and surfaceaccordee is not None else 0.1,
            "surfacecentremedical":surfacecentremedical if surfacecentremedical !=0 and surfacecentremedical is not None else 0.1,
            "loyermensuel":loyermensuel if loyermensuel !=0 and loyermensuel is not None else 0.1,
            "surfacecommunes":surfacecommunes if surfacecommunes !=0 and surfacecommunes is not None else 0.1,
            "pourcentagesalaire":pourcentagesalaire if pourcentagesalaire!=0 and pourcentagesalaire is not None else 0.1,
            "pourcentagechargessociales":pourcentagechargessociales if pourcentagechargessociales!=0 and pourcentagechargessociales is not None else 0.1,
            "salairepersonnel":salairepersonnel if salairepersonnel!=0 and salairepersonnel is not None else 0.1,
            "pourcentagechargessociales":pourcentagechargessociales if pourcentagechargessociales!=0 and pourcentagechargessociales is not None else 0.1,
            "surfaceaccordee":surfaceaccordee if surfaceaccordee!=0 and surfaceaccordee is not None else 0.1
        }
        
        return dict_to_return
    except:
        return None

def get_frais_materiel_df(doctorname):
    composite_df = pd.DataFrame(columns=['Charges','Cout Mensuel','Cout Annuel'])
    
    composite_df.set_index('Charges',inplace=True)
    #print(composite_df)
    dataa=fetch_doctor_info(doctorname)

    informatique_ann=dataa["informatique"]/dataa["nbmedicinsrepartirfrais"]
    informatique_men=informatique_ann/12

    assurance_ann=dataa["assurances"]/dataa["nbmedicinsrepartirfrais"]
    assurance_men=assurance_ann/12

    blanchisserie_ann=dataa["blanchisserie"]/dataa["nbmedicinsrepartirfrais"]
    blanchisserie_men = blanchisserie_ann/12

    logicielaxenita_ann=dataa["logicielaxenita"]/dataa["nbmedicins"]
    logicielaxenita_men=logicielaxenita_ann/12

    telephonieinternet_ann=dataa["telephonieinternet"]/dataa["nbmedicinsrepartirfrais"]
    telephonieinternet_men=telephonieinternet_ann/12

    simplify_ann=dataa["simplify"]/3
    simplify_men=simplify_ann/12

    conciergerie_ann=dataa["conciergerie"]/dataa["nbmedicinsrepartirfrais"]
    conciergerie_men = conciergerie_ann/12

    nettoyage_ann=dataa["nettoyage"]/dataa["nbmedicinsrepartirfrais"]
    nettoyage_men=nettoyage_ann/12

    loyersurfacecom_ann=dataa["surfacecommunes"]*(dataa["loyermensuel"]*12)/(dataa["surfacecentremedical"])*(dataa["surfaceaccordee"]/dataa["surfacecentremedical"])
    loyersurfacecom_men=loyersurfacecom_ann/12

    personnelsalaire_men=dataa["salairepersonnel"]*(dataa["pourcentagesalaire"]/100)
    personnelsalaire_ann=personnelsalaire_men*13

    chargesociales_men=personnelsalaire_men*dataa["pourcentagechargessociales"]/100
    chargesociales_ann=chargesociales_men*13

    prixloyersurfacem2_ann=dataa["surfaceaccordee"]*((dataa["loyermensuel"]*12)/(dataa["surfacecentremedical"]))
    prixloyersurfacem2_men=prixloyersurfacem2_ann/12
    

    temp_df2 = pd.DataFrame({
                "Cout Mensuel": [informatique_men,assurance_men,blanchisserie_men,logicielaxenita_men,telephonieinternet_men,simplify_men,conciergerie_men,nettoyage_men,loyersurfacecom_men,personnelsalaire_men,chargesociales_men,prixloyersurfacem2_men],
                "Cout Annuel":[informatique_ann,assurance_ann,blanchisserie_ann,logicielaxenita_ann,telephonieinternet_ann,simplify_ann,conciergerie_ann,nettoyage_ann,loyersurfacecom_ann,personnelsalaire_ann,chargesociales_ann,prixloyersurfacem2_ann]},
                index=["Informatique","Assurances","Blanchisserie","Axenita","TelePhonie Internet","Simplify","Conciergerie","Nettoyage","Loyer Surface Commune","Personnel  {0}% 13 Salaires".format(str(dataa["pourcentagesalaire"])),"Charges Sociale {0}%".format(str(dataa["pourcentagechargessociales"])),"Prix du loyer surface m2"])

    composite_df=pd.concat([composite_df, temp_df2])

    return composite_df

def get_dr_details(doctorname):
    search_query="""select SUM(somme) as Summation from facturation where facturationNom = 'Dr Diana' and facturationType='Facturation médecins'"""
    


@app.route('/reporting',methods=['GET','POST'])
@login_required
def reporting():

    #print(paymentdf)
    form=MainReportForm()
    ind_doctor_form=IndividualDoctorReportForm()
    choices=[]
    #choices.append(("---","---"))
    choices=choices+[(doctor.doctorname,doctor.doctorname)for doctor in db.engine.execute("select doctorname from doctor where isActive=1").fetchall()]   
    ind_doctor_form.doctorname.choices=choices


    if ind_doctor_form.validate_on_submit():
        current_date=datetime.datetime.now()
        current_num_timestamp="{0}{1}{2}_{3}{4}{5}".format(current_date.year,current_date.month,current_date.day,current_date.hour,current_date.minute,current_date.second)
        doctor_report_filename=r'{0}\reporting_temporary\RAPPORT_MEDECINS_{1}.pdf'.format(file_download_location,current_num_timestamp)
        dfs=[]

        varying_paymentslist=db.engine.execute("""select paimentnom AS PaiementNom,doctorpaiementsomme AS Somme,date AS Date FROM doctorpayment where doctorname='{0}' and YEAR(date)={1}""".format(ind_doctor_form.doctorname.data,ind_doctor_form.year.data))
        varying_paymentsdf=convert_list_to_dataframe(varying_paymentslist)
        varying_paymentsdf.set_index("PaiementNom",inplace=True)

        dfs.append((varying_paymentsdf.fillna(0).round(2),"Paeiment Medcins"))

        composite_df=get_frais_materiel_df(ind_doctor_form.doctorname.data)
        #print(composite_df)

        dfs.append((composite_df.fillna(0).round(2),"Charges Mensuel/Annuel"))

        leasinglist=db.engine.execute("""Select locationNom as LocationNom,
debut as Debut,
finPrevue as FinPrevue,
paiementinitial as "Paiement Initial",
paiement as PaiementMensuel,
paiement*12 as PaiementAnnuel
From leasing
where docteur='{0}'""".format(ind_doctor_form.doctorname.data))
        leasingdf=convert_list_to_dataframe(leasinglist)
        leasingdf.set_index("LocationNom",inplace=True)

        dfs.append((leasingdf.fillna(0).round(2),"Locations(Leasing)"))

        percentagelist=db.engine.execute("""
        select 
de as DE,
a as A,
pourcentages as Pourcentages,
sum( isNull((a-(de-1000))*(pourcentages/100), 0) ) over (order by de) as "Revenu annuel brut",
sum( isNull((a-(de-1000))*(pourcentages/100), 0) ) over (order by de)*100/a as "Pourcentage net de charges",
a-sum( isNull((a-(de-1000))*(pourcentages/100), 0) ) over (order by de) as "Mon Revenu annuel"



from percentageactivity where docteur='{0}'
        """.format(ind_doctor_form.doctorname.data))
        percentagedf=convert_list_to_dataframe(percentagelist)
        #percentagedf.set_index("LocationNom",inplace=True)

        dfs.append((percentagedf.fillna(0).round(2),"Pourcentage D'activite"))        


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
	SUM (CASE WHEN Month(date)=1 THEN somme END) AS Janvier,
	SUM (CASE WHEN Month(date)=2 THEN somme END) AS Février,
	SUM (CASE WHEN Month(date)=3 THEN somme END) AS Mars,
	SUM (CASE WHEN Month(date)=4 THEN somme END) AS Avril,
	SUM (CASE WHEN Month(date)=5 THEN somme END) AS Mai,
	SUM (CASE WHEN Month(date)=6 THEN somme END) AS Juin,
	SUM (CASE WHEN Month(date)=7 THEN somme END) AS Juillet,
	SUM (CASE WHEN Month(date)=8 THEN somme END) AS Aout,
	SUM (CASE WHEN Month(date)=9 THEN somme END) AS Septembre,
	SUM (CASE WHEN Month(date)=10 THEN somme END) AS Octobre,
	SUM (CASE WHEN Month(date)=11 THEN somme END) AS Novembre,
	SUM (CASE WHEN Month(date)=12 THEN somme END) AS Décembre,
    SUM (somme) AS TOTAL

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

        rowstmp=len(encaissementdf.index)
        enc1df=encaissementdf.iloc[:int(rowstmp/2)]
        enc2df=encaissementdf.iloc[int(rowstmp/2):]
        
        #dfs.append((encaissementdf.fillna(0).round(2),encaissementgraphdf.fillna(0).round(2),"Encaissement"))
        
        dfs.append((enc1df.fillna(0).round(2),encaissementgraphdf.fillna(0).round(2),"Encaissement"))
        dfs.append((enc2df.fillna(0).round(2),encaissementgraphdf.fillna(0).round(2),"Encaissement"))

        '''facturationlist = db.engine.execute("""select facturationType, SUM(somme) AS somme ,MONTH(date) AS "month",YEAR(date) as "year" From facturation where YEAR(date)={0} group by YEAR(date),MONTH(date) , facturationType""".format(form.year.data))
        
        facturationdf=convert_list_to_dataframe(facturationlist)
        facturationdf.set_index('facturationType',inplace=True)'''
        facturationgraphlist=db.engine.execute("""select facturationType, SUM(somme) AS somme ,YEAR(date) as "year" From facturation where YEAR(date)={0} group by YEAR(date) , facturationType""".format(form.year.data))
        facturationgraphdf=convert_list_to_dataframe(facturationgraphlist)
        facturationgraphdf.set_index('facturationType',inplace=True)

        facturationforreportlist=db.engine.execute("""SELECT facturationType AS FacturationType, 
	SUM (CASE WHEN Month(date)=1 THEN somme END) AS Janvier,
	SUM (CASE WHEN Month(date)=2 THEN somme END) AS Février,
	SUM (CASE WHEN Month(date)=3 THEN somme END) AS Mars,
	SUM (CASE WHEN Month(date)=4 THEN somme END) AS Avril,
	SUM (CASE WHEN Month(date)=5 THEN somme END) AS Mai,
	SUM (CASE WHEN Month(date)=6 THEN somme END) AS Juin,
	SUM (CASE WHEN Month(date)=7 THEN somme END) AS Juillet,
	SUM (CASE WHEN Month(date)=8 THEN somme END) AS Aout,
	SUM (CASE WHEN Month(date)=9 THEN somme END) AS Septembre,
	SUM (CASE WHEN Month(date)=10 THEN somme END) AS Octobre,
	SUM (CASE WHEN Month(date)=11 THEN somme END) AS Novembre,
	SUM (CASE WHEN Month(date)=12 THEN somme END) AS Décembre,
    SUM (somme) AS TOTAL

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


        query_for_general_table = db.engine.execute("""select

doctorname as "docteurNom",
doctorspeciality as Specialite,
nblocaux as "No local",
surfacecentremedical as "m2"

from doctor""")

        maindf=convert_list_to_dataframe(query_for_general_table)
        maindf.set_index('docteurNom',inplace=True) 
        
        current_date=datetime.datetime.now()

        current_num_timestamp="{0}{1}{2}_{3}{4}{5}".format(current_date.year,current_date.month,current_date.day,current_date.hour,current_date.minute,current_date.second)
        report_filename=r'{0}\reporting_temporary\RAPPORT_{1}.pdf'.format(file_download_location,current_num_timestamp)
        
        dataframe_to_pdf(dfs,pnl.round(2),form.year.data,report_filename,enctotal.round(2),paymenttotal.round(2),maindf)        

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