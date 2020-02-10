import datetime

import markdown
from flask import (
    Flask, render_template, redirect, g, session, current_app, abort, url_for, request, flash
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers import Response

from models import database, Key, Post
from forms import KeyForm, ChangeKeyForm, PostForm
from crud import all_posts, public_posts
from utils import redirect_back


def get_object_by_id_or_404(model, id, **kwargs):
    try:
        return model.get_by_id(id)
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
    if request.method == 'GET' and session.get('logged_in'):
        return redirect_back('home')
    form = KeyForm()
    if request.method == 'POST' and form.validate_on_submit():
        key = form.key.data
        if check_password_hash(Key.get_by_id(1).key, key):
            session['logged_in'] = True
            flash('<script>alert("登陆认证成功")</script>')
            return redirect(url_for('home'))
        else:
            flash('<script>alert("密码验证失败")</script>')
    return render_template('login.html', form=form)


@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))


def home():
    if session.get('logged_in'):
        posts = all_posts()
    else:
        posts = public_posts()
    return render_template('home.html', posts=posts)


def detail(id: int):
    if session.get('logged_in'):
        post = get_object_by_id_or_404(Post, id)
    else:
        post = get_object_by_id_or_404(Post, id=id, is_public=True)
    post.content = markdown.markdown(post.content,
                                    extensions=['markdown.extensions.extra',
                                                'markdown.extensions.codehilite'])
    post.pub_date = post.pub_date.strftime('%Y-%m-%d')
    return render_template('detail.html', post=post)


@login_required
def update(id: int):
    post = get_object_by_id_or_404(Post, id=id)
    checked = "checked" if post.is_public else ""
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            with database.atomic():
                post.title = form.title.data
                post.content = form.content.data
                post.is_public = form.is_public.data
                post.pub_time = datetime.datetime.now()
                post.save()
                return redirect(url_for('detail', id=post.id))
    return render_template('update.html', post=post, form=form, checked=checked)


@login_required
def delete(id: int):
    post = get_object_by_id_or_404(Post, id=id)
    with database.atomic():
        Post.delete_instance(post)
    flash('<script>alert("删除成功")</script>')
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
            flash('<script>alert("添加成功")</script>')
            return redirect(url_for('detail', id=post.id))
    return render_template('add.html', form=form)


@login_required
def change_key():
    form = ChangeKeyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            key = Key.get_by_id(1)
            key.key = generate_password_hash(form.ckey.data)
            key.save()
            flash('<script>alert("密码修改成功")</script>')
            return redirect(url_for('home'))
        else:
            flash('<script>alert("密码修改失败，请确保两次输入一致")</script>')
    return render_template('change_key.html', form=form)


import random
def about():
    color = random.choice(['red', 'orange', 'green', 'skyblue', 'pink', 'purple'])
    return f'<span style="color:{color};">QQ:286183317</span>'


def favicon() -> Response:
    return current_app.send_static_file('images/favicon.ico')


def before_request():
    g.db = database
    g.db.connect()


def after_request(response):
    g.db.close()
    return response


def not_found(error: Exception) -> (str, int):
    return render_template("404.html"), 404


def _jinja2_filter_datetime(date, fmt=None):
    format_='%Y-%m-%d'
    return date.strftime(format_)


def init_app(app: Flask) -> None:
    @app.context_processor
    def _inject_logged_in(): # 是否已登录
        logged_in = session.get('logged_in', False)
        return dict(logged_in=logged_in)


    app.add_url_rule('/', 'home', home)
    app.add_url_rule('/favicon.ico', 'favicon', favicon)
    app.add_url_rule('/add', 'add', add, methods=['GET', 'POST'])
    app.add_url_rule('/delete/<int:id>', 'delete', delete)
    app.add_url_rule('/update/<int:id>', 'update', update, methods=['GET', 'POST'])
    app.add_url_rule('/detail/<int:id>', 'detail', detail)
    app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/change_key', 'change_key', change_key, methods=['GET', 'POST'])
    app.add_url_rule('/about', 'about', about)

    app.before_request(before_request)
    app.after_request(after_request)

    app.add_template_filter(_jinja2_filter_datetime, 'strftime')

    app.register_error_handler(404, not_found)
