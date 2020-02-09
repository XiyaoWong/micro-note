import datetime

import markdown
from flask import (
    Flask, render_template, redirect, g, session, current_app, abort, url_for, request
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers import Response

from .models import database, Key, Post
from .forms import KeyForm, ChangeKeyForm, PostForm
from .crud import all_posts, public_posts
from .utils import redirect_back


def get_object_or_404(model, **expressions):
    try:
        return model.get(**expressions)
    except model.DoesNotExist:
        abort(404)


def login_required(f):
    # @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner


def login():
    form = KeyForm()
    if form.validate_on_submit():
        key = form.key.data
        if check_password_hash(Key.get_by_id(1).key, key):
            session['logged_in'] = True
            return redirect_back('home')
    return render_template('login.html', form=form)


# def logout():
#     session.pop('logged_in', None)
#     return redirect(url_for('home'))


def home():
    if session.get('logged_in'):
        posts = all_posts()
    else:
        posts = public_posts()
    
    return render_template('home.html', posts=posts)


def detail(id: int):
    if session['logged_in']:
        post = get_object_or_404(Post, id=id)
    else:
        post = get_object_or_404(Post, id=id, is_public=True)

    post.content = markdown.markdown(post.content,
                                    extensions=['markdown.extensions.extra',
                                                'markdown.extensions.codehilite'])
    return render_template('detail.html', post=post)


@login_required
def update(id: int):
    post = get_object_or_404(Post, id=id)
    form = PostForm()
    if form.validate_on_submit:
        with database.atomic():
            post.title = form.title.data
            post.content = form.content.data
            post.is_public = form.is_public.data
            post.pub_time = datetime.datetime.now()
            return redirect(url_for('detail', id=post.id))
    return render_template('update.html', post=post, form=form)
    

@login_required
def delete(id: int):
    post = get_object_or_404(Post, id=id)
    with database.atomic():
        Post.delete_instance(post)
    return redirect(url_for('home'))


@login_required
def add():
    form = PostForm()
    if form.validate_on_submit():
        with database.atomic():
            post = Post.create(
                title = form.title.data,
                content = form.content.data,
                is_public = form.is_public.data,
                pub_date = datetime.datetime.now(),)
            return redirect(url_for('detail', id=post.id))
    return render_template('add.html', form=form)


def favicon() -> Response:
    return current_app.send_static_file('images/favicon.ico')


def before_request():
    g.db = database
    g.db.connect()


def after_request(response):
    g.db.close()
    return response


def init_app(app: Flask) -> None:
    app.add_url_rule('/', 'home', home)
    app.add_url_rule('/favicon.ico', 'favicon', favicon)
    app.add_url_rule('/add', 'add', add)
    app.add_url_rule('/delete/<int:id>', 'delete', delete)
    app.add_url_rule('/update/<int:id>', 'update', update)
    app.add_url_rule('/detail/<int:id>', 'detail', detail)

    app.before_request(before_request)
    app.after_request(after_request)