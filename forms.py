from DB_layer import *
from flask import Flask, render_template, url_for,redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,Label,BooleanField
from wtforms.validators import InputRequired,Length,ValidationError,DataRequired
from flask_bcrypt import Bcrypt
from app import *



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

class AddDoctorForm(FlaskForm):    
    doctorname=StringField(label="Doctor Name ",validators=[InputRequired()],render_kw={"placeholder":"Doctor Name"})
    doctorspeciality=StringField(label="Doctor Speciality ",validators=[InputRequired()],render_kw={"placeholder":"Doctor Speciality"})
    #isActive=StringField(label="Is Active ",validators=[InputRequired()],render_kw={"placeholder":"Active"})
    percentageShare=StringField(label="Percentage Share ",validators=[InputRequired()],render_kw={"placeholder":"Percentage Share"})
    isActive = BooleanField('Active?')

    submit =SubmitField("Submit")




