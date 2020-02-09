from peewee import Model, SqliteDatabase, CharField, TextField, DateTimeField, BooleanField

from .config import DATABASE


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