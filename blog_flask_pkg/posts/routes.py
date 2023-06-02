from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from blog_flask_pkg import db
from blog_flask_pkg.models import Post
from blog_flask_pkg.posts.forms import PostForm

posts = Blueprint('posts',__name__)



@posts.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created!',"success")
        return redirect(url_for('main.home'))
    print(form.errors)
    return render_template('create_post.html',title='New Post', form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update",methods=['GET','POST'])
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
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method=='GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post', form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete",methods=['POST','GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted Successfully',"success")
    return redirect(url_for('main.home'))