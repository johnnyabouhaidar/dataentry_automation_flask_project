from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,Label,BooleanField
from app import *

class Doctor(db.Model):
    doctorid=db.Column(db.Integer,primary_key=True)
    doctorname=db.Column(db.String(80),nullable=False,unique=True)
    doctorspeciality=db.Column(db.String(80),nullable=False)
    isActive = db.Column(db.Boolean,nullable=False)
    percentageShare = db.Column(db.Float,nullable=False)

class AddDoctorForm(FlaskForm):    
    doctorname=StringField(label="Doctor Name ",validators=[InputRequired()],render_kw={"placeholder":"Doctor Name"})
    doctorspeciality=StringField(label="Doctor Speciality ",validators=[InputRequired()],render_kw={"placeholder":"Doctor Speciality"})
    #isActive=StringField(label="Is Active ",validators=[InputRequired()],render_kw={"placeholder":"Active"})
    percentageShare=StringField(label="Percentage Share ",validators=[InputRequired()],render_kw={"placeholder":"Percentage Share"})
    isActive = BooleanField('Active?')

    submit =SubmitField("Submit")


