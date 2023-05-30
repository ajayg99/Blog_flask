from flask import Flask, render_template, url_for, flash, redirect, request
from blog_flask_pkg.forms import Reg, Log
from blog_flask_pkg.models import Post, User
from blog_flask_pkg import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


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


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')