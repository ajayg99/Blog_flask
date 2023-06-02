from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog_flask_pkg import db, bcrypt
from blog_flask_pkg.models import User, Post
from blog_flask_pkg.users.forms import Reg, Log, Update_acc, RequestResetForm, ResetPasswordForm
import os, requests

from blog_flask_pkg.users.utils import send_reset_email
users = Blueprint('users',__name__)


@users.route('/register', methods=['GET','POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = Reg()        #instance of Reg from forms.py
    if form.validate_on_submit():
        print("success")
        hashed_pw = bcrypt.generate_password_hash(form.passw.data).decode('utf-8') #hashing password
        #pushing data to DB
        user = User(username=form.uname.data, email=form.email.data, passw=hashed_pw) 
        db.session.add(user)
        db.session.commit()

        #getting default img from robohash which is generated in models.py when creating user profile ; the url is a field(img) for the user table
        #the logic stores the img under the dir named after user
        user_data = User.query.filter_by(username=form.uname.data).first()
        img = user_data.img
        response = requests.get(img)
        if response.status_code == 200:
            filename = 'default'
            path = './blog_flask_pkg/static/Users/'+str(user_data.username)+'/profile_pics'
            if not os.path.exists(path):
                os.makedirs(path)
            file_path = os.path.join(path, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)

        flash(f'Account created successfully { form.uname.data }','success')
        return redirect(url_for('users.Login'))
    #print(form.errors) testing
    #print("failed")
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET','POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Log()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.uname.data).first()
        if user and bcrypt.check_password_hash(user.passw, form.passw.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')    #using get because it returns null if next doesn't exist
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('login unsuccessful',"danger")
    #print(form.errors) testing
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = Update_acc()
    if form.validate_on_submit():

        if form.pic.data:

            path = './blog_flask_pkg/static/Users/'+str(current_user.username)+'/profile_pics/default'
            form.pic.data.save(path)
            
        os.rename('./blog_flask_pkg/static/Users/'+current_user.username, './blog_flask_pkg/static/Users/'+form.uname.data)
        current_user.username = form.uname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated',"success")
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.uname.data = current_user.username
        form.email.data = current_user.email
    img = url_for('static',filename='Users/'+current_user.username+'/profile_pics/default')
    return render_template('account.html', title='Account', img=img, form=form)



@users.route("/user/<string:username>",methods=['POST','GET'])
@login_required
def user_post(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1,type=int)
    post = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('user_post.html', posts=post, user=user)


@users.route("/reset_password",methods=['POST','GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email send for password reset',"info")
        return redirect(url_for('users.Login'))
    return render_template('reset_request.html',title="Reset Password", form=form)

@users.route("/reset_password/<token>",methods=['POST','GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user= User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token',"warning")
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.passw.data).decode('utf-8') #hashing password
        user.passw = hashed_pw
        db.session.commit()
        flash(f'Password Reset Successfull','success')
        return redirect(url_for('users.Login'))
    return render_template('reset_token.html',title="Reset Password", form=form)