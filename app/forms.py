from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed



class MerchantLogin(FlaskForm):

    email = StringField('Email', 
        validators=[DataRequired(), Email(), InputRequired()], 
        description="123@abc.com")

    password = PasswordField('Password', 
        validators=[DataRequired(), InputRequired()])



class MerchantRegistration(FlaskForm):
    name = StringField('Company Name', 
        validators=[DataRequired(), InputRequired()])

    address = StringField('Company Address', 
        validators=[DataRequired(), InputRequired()])

    location = StringField('Location', 
        validators=[DataRequired(), InputRequired()], 
        description="kingston, Jamaica")

    email = StringField('Email', 
        validators=[DataRequired(), Email(), InputRequired()], 
        description="123@abc.com")

    password = PasswordField('Password', 
        validators=[DataRequired(), InputRequired()])

    confirmPassword = PasswordField('Confirm Password', 
        validators=[DataRequired(), InputRequired()])
    
    estWaitTime = IntegerField('Estimated Wait Time', 
        validators=[],
        description="Set to 10 minutes by default")
    
    logo = FileField('Company Logo', 
        validators=[FileRequired(),
        FileAllowed(['jpg', 'png', 'Images only!'])])

class TicketCheck(FlaskForm):

    customer_code = StringField('Access Code', 
        validators=[DataRequired(), InputRequired()], 
        description="The code the custimer was given when they joined the line")

  

    
    
    