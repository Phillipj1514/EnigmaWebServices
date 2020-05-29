from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed



class profileForm(FlaskForm):
    first_name = StringField('First Name', 
        validators=[DataRequired(), InputRequired()])

    last_name = StringField('Last Name', 
        validators=[DataRequired(), InputRequired()])

    gender = SelectField('Gender',
        validators=[DataRequired()],
        choices=[('Male', 'Male'), ('Female', 'Female')], 
        default=('male','Male'))

    email = StringField('Email', 
        validators=[DataRequired(), Email(), InputRequired()], 
        description="123@abc.com")

    location = StringField('Location', 
        validators=[DataRequired(), InputRequired()], 
        description="kingston")

    biography  = TextAreaField('Biography',
        validators=[DataRequired(), InputRequired()])

    image = FileField('Profile Picture', 
        validators=[FileRequired(),
        FileAllowed(['jpg', 'png', 'Images only!'])])
