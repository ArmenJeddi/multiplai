from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, PasswordField
from wtforms.validators import DataRequired, Email

class DueDiligenceForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pdf = FileField('PDF', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit_due_diligence = SubmitField("Let's do your due diligence")

class ContactForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    question = TextAreaField('Question', validators=[DataRequired()])
    submit_contact = SubmitField('Contact Us')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
