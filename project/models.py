import getpass

from peewee import Model, SqliteDatabase, CharField, TextField, DateTimeField, BooleanField
from werkzeug.security import generate_password_hash

from config import DATABASE


database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class Key(BaseModel):
    key = CharField()


class Post(BaseModel):
    title = CharField()
    content = TextField(default='')
    pub_date = DateTimeField()
    is_public = BooleanField(default=True)


def create_tables():
    with database:
        database.create_tables([Key, Post])
    
    key = generate_password_hash('123456')
    database.connect()
    Key.create(key=key)
    database.close()
    print('首次创建数据库，默认密码为123456，请尽快修改！')