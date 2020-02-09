# 增删改查 函数
from models import Key, Post


def public_posts():
    return (Post
            .select()
            .where(Post.is_public == True)
            .order_by(Post.pub_date.desc()))


def private_posts():
    return (Post
        .select()
        .where(Post.is_public == False)
        .order_by(Post.pub_date.desc()))


def all_posts():
    return (Post
            .select()
            .order_by(Post.pub_date.desc()))