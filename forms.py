from wsgiref.validate import validator
from DB_layer import *
from flask import Flask, render_template, url_for,redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms.widgets import TextArea
from wtforms import StringField,PasswordField,SubmitField,Label,BooleanField,FloatField,SelectField,DateField,SelectMultipleField,IntegerField,SearchField 
from wtforms.validators import InputRequired,Length,ValidationError,DataRequired,NumberRange
from flask_bcrypt import Bcrypt
from app import *



class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})
    access = SelectMultipleField('Roles (Utilisez "Ctrl" pour plusieurs rôles)',validators=[InputRequired()], choices=[('setup','Setup'),('doctors','Docteurs'),('payments','Paiements'),('facturation','Facturations'),('dentisterie','Dentisterie'),('encaissement','Encaissement'),('fraismateriel','Frais Materiel'),('paiement_medecin','Paiement du médecin'),('reports','Reports Generation')])
    isAdmin = BooleanField('Admin?')

    submit =SubmitField("Register")

    def validate_username(self,username):
        existing_user_username = User.query.filter_by(
            username=username.data
        ).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )
class EditRegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Username"})
    password=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})
    access = SelectMultipleField('Roles (Use Ctrl for multiple roles)',validators=[InputRequired()], choices=[('setup','Setup'),('doctors','Docteurs'),('payments','Paiements'),('facturation','Facturations'),('dentisterie','Dentisterie'),('encaissement','Encaissement'),('fraismateriel','Frais Materiel'),('paiement_medecin','Paiement du médecin'),('reports','Reports Generation')])
    isAdmin = BooleanField('Admin?')

    submit =SubmitField("Register")


class LoginForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})

    submit=SubmitField("Login")

class AddDoctorForm(FlaskForm):    
    doctorname=StringField(label="Docteur Nom ",validators=[InputRequired()],render_kw={"placeholder":"Doctor Name"})
    doctorspeciality=StringField(label="Docteur Spécialité ",validators=[InputRequired()],render_kw={"placeholder":"Doctor Speciality"})
    #isActive=StringField(label="Is Active ",validators=[InputRequired()],render_kw={"placeholder":"Active"})
    percentageShare=FloatField(label="Part en pourcentage ",validators=[InputRequired()],render_kw={"placeholder":"Percentage Share"})
    isActive = BooleanField('Active?')
    conditionsfinanciers=StringField('Conditions Financieres',widget=TextArea())

    submit =SubmitField("Submit")

class AddDoctorConstantsForm(FlaskForm):
    doctorname=StringField(label="Docteur Nom ",validators=[InputRequired()],render_kw={"placeholder":"Doctor Name"})
    doctorspeciality=StringField(label="Docteur Spécialité ",validators=[InputRequired()],render_kw={"placeholder":"Doctor Speciality"})
    #isActive=StringField(label="Is Active ",validators=[InputRequired()],render_kw={"placeholder":"Active"})
    percentageShare=FloatField(label="Part en pourcentage ",validators=[InputRequired()],render_kw={"placeholder":"Percentage Share"})
    isActive = BooleanField('Active?')
    conditionsfinanciers=StringField('Conditions Financieres',widget=TextArea())

    pourcentagesalaire=FloatField(label="Pourcentage Salaire")
    pourcentagechargessociales=FloatField(label="Pourcentage Charges Sociales")
    surfacecentremedical = FloatField(label="Surface Centre medical en M2")
    surfacecommunes=FloatField(label="Surface Communes en M2")
    loyermensuel=FloatField(label="Loyer Mensuel")
    surfaceaccordee=FloatField(label="Surface Accordee")
    nettoyage=FloatField(label="Nettoyage Bureau/an")
    conciergerie=FloatField(label="Conciergerie")
    salairepersonnel=FloatField(label="Salaire Personnel a 100%/mois")
    telephonieinternet=FloatField(label="Telephonie-Internet")
    logicielaxenita=FloatField(label="Logiciel Axenita")
    nbmedicins=FloatField(label="Nb de medecins pour axenita")
    assurances =FloatField(label="Assurances/annuel")
    blanchisserieleman=FloatField(label="Blanchisserie du leman/annuel")
    informatique=FloatField(label="Informatique/annuel")
    nblocaux=FloatField(label="Nb de Locaux")
    nbmedicinsrepartirfrais=FloatField(label="Nb de medecins pour repartir frais")
    receptionniste=FloatField(label="Receptionniste annuel")
    Apprentie=FloatField(label="Apprentie de 2eme annee")
    simplify=FloatField(label="Simplify")
    steriswiss=FloatField(label="Steriswiss")
    submit =SubmitField("Submit")


class AddDoctorPaymentForm(FlaskForm):
    doctorname=SelectField("Doctor Name",choices=[],validators=[InputRequired()])
    paimentnom=SelectField("Paiement Nom",choices=[],validators=[InputRequired()])
    paimentnomALT=StringField("Nouveau Paiement?",render_kw={"placeholder":"Paiement Nom"})
    date=DateField(label="Date",validators=[InputRequired()])
    
    doctorpaiementsomme = FloatField(label="Somme",validators=[InputRequired()],render_kw={"placeholder":"Somme"})

    submit=SubmitField("Submit")

class Addpaymenttype(FlaskForm):
    paymenttype=StringField(label="Paiement Type ",validators=[InputRequired()],render_kw={"placeholder":"(i.e: Charges Fixes...)"})

    submit =SubmitField("Submit")


class AddPaymentForm(FlaskForm):
    paiementsType= SelectField('PaiementsType',choices=[],validators=[InputRequired()])
    paiementsNom = SelectField('PaiementsNom',choices=[],validators=[InputRequired()])

    paiementsNomALT = StringField(label="Nouveau paiement ?",render_kw={"placeholder":"paiementsNom"})
    somme = FloatField(label="Somme",validators=[InputRequired()],render_kw={"placeholder":"Somme"})
    date = DateField(label="Paiement Date",validators=[InputRequired()],render_kw={"placeholder":"Date"})

    comment=StringField('Comment',widget=TextArea())

    submit = SubmitField("Submit")

class AddDentistrytype(FlaskForm):
    dentisterieType=StringField(label='Dentisterie Type',validators=[InputRequired()],render_kw={"placeholder":"(i.e: Facturation hygiéniste...)"})

    submit=SubmitField("Submit")

class AddDentistryInfoForm(FlaskForm):
    dentisterieType=SelectField('DentisterieType',choices=[],validators=[InputRequired()])
    dentisterieNom=SelectField('DentisterieNom',choices=[],validators=[InputRequired()])

    dentisterieNomALT =StringField(label='Nouveau Dentistrie Info',render_kw={"placeholder":"dentistrieInfoNom"})
    somme = FloatField(label="Somme",validators=[InputRequired()],render_kw={"placeholder":"Somme"})
    date=DateField(label="Date",validators=[InputRequired()],render_kw={"placeholder":"Date"})

    submit=SubmitField("Submit")

class AddFacturationtype(FlaskForm):
    facturationtype=StringField(label="Facturation Type ",validators=[InputRequired()],render_kw={"placeholder":"(i.e: Facturation dentiste...)"})

    submit =SubmitField("Submit")

class AddFacturationForm(FlaskForm):
    facturationType= SelectField('FacturationType',choices=[],validators=[InputRequired()])
    facturationNom = SelectField('FacturationNom',choices=[],validators=[InputRequired()])

    facturationNomALT = StringField(label="Nouveau facturation ?",render_kw={"placeholder":"facturationNom"})
    somme = FloatField(label="Somme",validators=[InputRequired()],render_kw={"placeholder":"Somme"})
    date = DateField(label="Facturation Date",validators=[InputRequired()],render_kw={"placeholder":"Date"})
    comment=StringField('Comment',widget=TextArea())

    submit = SubmitField("Submit")

class AddFraismaterieltype(FlaskForm):
    fraismaterieltype=StringField(label="Frais Meteriel Type ",validators=[InputRequired()],render_kw={"placeholder":"Type"})

    submit =SubmitField("Submit")

class AddFraismaterielForm(FlaskForm):
    fraismaterieltype=SelectField('Frais Materiel Type',choices=[],validators=[InputRequired()])
    fraismaterielnom=SelectField('Frais Materiel Nom',choices=[],validators=[InputRequired()])
    fraismaterielnomALT=StringField('Nouveau Frais Materiel?',render_kw={"placeholder":"Frais Materiel"})
    fraismaterielsomme=FloatField("Somme",validators=[InputRequired()],render_kw={"placeholder":"Somme"})
    fraismaterieldate=DateField('Date',validators=[InputRequired()])
    comment=StringField('Comment',widget=TextArea())

    submit = SubmitField("Submit")

class AddEncaissementForm(FlaskForm):
    encaissementNom=SelectField('Encaissement Nom',choices=[])
    encaissementNomALT = StringField(label="Nouveau encaissement ?")
    encaissementDate=DateField(label="Encaissement Date",validators=[InputRequired()])
    montant=FloatField(label="montant",validators=[InputRequired()])
    banque=SelectField('Banque',choices=[('UBS','UBS'),('Postfinance ','Postfinance')])
    comment=StringField('Comment',widget=TextArea())

    submit =SubmitField("Submit")

class MainReportForm(FlaskForm):
    year = IntegerField(label="An",validators=[InputRequired()],render_kw={"placeholder":"Year"})
    submit =SubmitField("Submit")

class IndividualDoctorReportForm(FlaskForm):
    doctorname=SelectField('Nom du médecin',choices=[])
    year = IntegerField(label="An",validators=[InputRequired()],render_kw={"placeholder":"Year"})

    doctor_submit=SubmitField("Submit")
    
class Export_to_excel(FlaskForm):

    export_submit=SubmitField("Exporter vers Excel")

class LeasingForm(FlaskForm):
    locationNom=StringField(label="Location(Leasing) Nom",validators=[InputRequired()])
    debut=DateField(label="Debut",validators=[InputRequired()])
    finPrevue=DateField(label="Fin Prevue",validators=[InputRequired()])
    paiement=FloatField(label="Paiement",validators=[InputRequired()])
    paiementinitial=FloatField(label="Paiement Initial",validators=[InputRequired()])

    leasesubmit=SubmitField("Submit")

class SearchForm(FlaskForm):
    searchstring=SearchField()
    #searchfilter=SelectField(choices=[("none","Filtrer par")])

    searchsubmit=SubmitField("🔍Chercher")
    #clearsearch=SubmitField("CLEAR")
    
class PercentageactivityForm(FlaskForm):
    de=IntegerField(label="De",validators=[InputRequired()],render_kw={"placeholder":"e.g. 0"})
    a=IntegerField(label="A",validators=[InputRequired()],render_kw={"placeholder":"e.g. 200000"})
    pourcentages=FloatField(label="Pourcentages",validators=[InputRequired()])

    submit=SubmitField("Submit")



