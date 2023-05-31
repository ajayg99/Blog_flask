from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField,SubmitField, BooleanField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError
from blog_flask_pkg.models import User
from flask import flash

class Reg(FlaskForm):
    uname = StringField('Username', validators=[DataRequired(),Length(min=4, max=20)])
    email = EmailField('Email',validators=[DataRequired(), Email()])
    passw = PasswordField('password',validators=[DataRequired()])
    confirm_passw = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('passw',message="password mismatch")])
    submit = SubmitField('Sign Up')

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

class Update_acc(FlaskForm):
    uname = StringField('Username', validators=[DataRequired(),Length(min=4, max=20)])
    email = EmailField('Email',validators=[DataRequired(), Email()])
    pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')

    def validate_uname(self,uname):
        if uname.data != current_user.username:
            user = User.query.filter_by(username=uname.data).first()
            if user:
                raise ValidationError('Username already exists')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('email already exists')
            
class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')