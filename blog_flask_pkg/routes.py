from flask import Flask, render_template, url_for, flash, redirect, request
from blog_flask_pkg.forms import Reg, Log, Update_acc
from blog_flask_pkg.models import Post, User
from blog_flask_pkg import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os, requests


post = [
    {
        'author':'ajay',
         'title' : 'devops',
         'content':'blogpost',
         'date_posted':'April 21, 2018'

    },
        {
        'author':'ajay',
         'title' : 'cloud',
         'content':'blogpost',
         'date_posted':'April 21, 2018'

    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=post)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register', methods=['GET','POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Reg()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.passw.data).decode('utf-8')
        user = User(username=form.uname.data, email=form.email.data, passw=hashed_pw)
        db.session.add(user)
        db.session.commit()

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
        return redirect(url_for('Login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Log()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.uname.data).first()
        if user and bcrypt.check_password_hash(user.passw, form.passw.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')    #using get because it returns null if next doesn't exist
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('login unsuccessful',"danger")
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = Update_acc()
    if form.validate_on_submit():
        os.rename('./blog_flask_pkg/static/Users/'+current_user.username, './blog_flask_pkg/static/Users/'+form.uname.data)
        current_user.username = form.uname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated',"success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.uname.data = current_user.username
        form.email.data = current_user.email
    img = url_for('static',filename='Users/'+current_user.username+'/profile_pics/default')
    return render_template('account.html', title='Account', img=img, form=form)