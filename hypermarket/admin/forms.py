from wtforms import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import required
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[required()])
    password = PasswordField('Password', validators=[required()])
