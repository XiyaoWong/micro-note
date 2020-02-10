from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, SubmitField, PasswordField 
from wtforms.validators import DataRequired, EqualTo, Length
# from flask_wtf.csrf import CsrfProtect


class KeyForm(FlaskForm):
    key = PasswordField(label='密码', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='确认')


class ChangeKeyForm(FlaskForm):
    key = PasswordField(label='密码', validators=[Length(min=6), DataRequired()])
    ckey = PasswordField(label='确认密码', validators=[Length(min=6), EqualTo('key'), DataRequired()])
    submit = SubmitField(label='确认')


class PostForm(FlaskForm):
    title = StringField(label='标题', validators=[DataRequired()])
    content = TextAreaField(label='正文')
    is_public = BooleanField(label='是否公开')
    submit = SubmitField(label='确认')


# csrf = CsrfProtect()