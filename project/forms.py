from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class KeyForm(FlaskForm):
    key = StringField(validators=[DataRequired()])


class ChangeKeyForm(FlaskForm):
    key = StringField(validators=[DataRequired()])
    ckey = EqualTo('key', '两次输入密码不一致')


class PostForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    content = TextField()
    is_public = BooleanField()