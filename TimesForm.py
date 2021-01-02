from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField

class TimesForm(FlaskForm):
   name = TextField("Name Of Student")
   submit = SubmitField("Submit")  
