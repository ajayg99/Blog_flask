
from flask import url_for
from flask_mail import Message
from blog_flask_pkg import mail
import os

def send_reset_email(user):
    token = user.get_reset_token()
    sender=str(os.environ.get('EMAIL_USER'))
    msg = Message('Password Reset Request', sender=sender, recipients=[user.email])
    msg.body = f'''To reset the passsword, visit the following link: { url_for('users.reset_token', token=token, _external=True) }. 
    If you did not make this request ignore the email and no changes will be made.'''
    mail.send(msg)