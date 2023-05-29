from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError
from blog_flask_pkg.models import User
from flask import flash
class Reg(FlaskForm):
    uname = StringField('Username', validators=[DataRequired(),Length(min=4, max=20)])
    email = EmailField('Email',validators=[DataRequired(), Email()])
    passw = PasswordField('password',validators=[DataRequired()])
    confirm_passw = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('passw',message="password mismatch")])
    submit = SubmitField('Sign_Up')

    def validate_uname(self,uname):
        user = User.query.filter_by(username=uname.data).first()
        if user:
            raise ValidationError('Username already exists')
    
    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('email already exists')

class Log(FlaskForm):
    uname = StringField('Username', validators=[DataRequired(),Length(min=2, max=20)])
    passw = PasswordField('password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')