from wsgiref.validate import validator
from DB_layer import *
from flask import Flask, render_template, url_for,redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,Label,BooleanField,FloatField,SelectField,DateField,SelectMultipleField
from wtforms.validators import InputRequired,Length,ValidationError,DataRequired,NumberRange
from flask_bcrypt import Bcrypt
from app import *



class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})
    access = SelectMultipleField('Roles (Use Ctrl for multiple roles)',validators=[InputRequired()], choices=[('doctors','Doctors'),('payments','Payments'),('reports','Reports Generation')])

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

class AddDoctorForm(FlaskForm):    
    doctorname=StringField(label="Doctor Name ",validators=[InputRequired()],render_kw={"placeholder":"Doctor Name"})
    doctorspeciality=StringField(label="Doctor Speciality ",validators=[InputRequired()],render_kw={"placeholder":"Doctor Speciality"})
    #isActive=StringField(label="Is Active ",validators=[InputRequired()],render_kw={"placeholder":"Active"})
    percentageShare=FloatField(label="Percentage Share ",validators=[InputRequired()],render_kw={"placeholder":"Percentage Share"})
    isActive = BooleanField('Active?')

    submit =SubmitField("Submit")

class Addpaymenttype(FlaskForm):
    paymenttype=StringField(label="Payment Type ",validators=[InputRequired()],render_kw={"placeholder":"(i.e: Charges Fixes...)"})

    submit =SubmitField("Submit")


class AddPaymentForm(FlaskForm):
    paiementsType= SelectField('PaiementsType',choices=[])
    paiementsNom = SelectField('PaiementsNom',choices=[])

    paiementsNomALT = StringField(label="Nouveau paiement ?",render_kw={"placeholder":"paiementsNom"})
    somme = FloatField(label="Somme",validators=[InputRequired()],render_kw={"placeholder":"Somme"})
    date = DateField(label="Paiement Date",validators=[InputRequired()],render_kw={"placeholder":"Date"})

    submit = SubmitField("Submit")



