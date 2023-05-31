from flask import Flask, render_template, url_for, flash, redirect, request, abort
from blog_flask_pkg.forms import Reg, Log, Update_acc, PostForm
from blog_flask_pkg.models import Post, User
from blog_flask_pkg import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os, requests


@app.route('/')
@app.route('/home')
@login_required
def home():
    page = request.args.get('page',1,type=int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('home.html', posts=post)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register', methods=['GET','POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = Reg()        #instance of Reg from forms.py
    if form.validate_on_submit():
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

        if form.pic.data:

            path = './blog_flask_pkg/static/Users/'+str(current_user.username)+'/profile_pics/default'
            form.pic.data.save(path)
            
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


@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created!',"success")
        return redirect(url_for('home'))
    return render_template('create_post.html',title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post Updated!',"success")
        return redirect(url_for('post',post_id=post.id))
    elif request.method=='GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted Successfully',"success")
    return redirect(url_for('home'))