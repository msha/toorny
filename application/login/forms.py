from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,validators

class RegisterForm(FlaskForm):

    name = StringField("Name")
    username = StringField("Username", [validators.Length(min=5)])
    password = PasswordField("Password", [validators.Length(min=8)])

    class Meta:
        csrf = False

class LoginForm(FlaskForm):

    username = StringField("Username")
    password = PasswordField("Password")
    
    class Meta:
        csrf = False