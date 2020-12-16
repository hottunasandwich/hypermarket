from wtforms import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import required
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField('نام کاریری', validators=[required()])
    password = PasswordField('رمز عبور', validators=[required()])