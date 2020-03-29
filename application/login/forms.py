from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,validators

class RegisterForm(FlaskForm):

    name = StringField("Name")
    username = StringField("Username", [validators.Length(min=5),validators.Length(max=30)])
    password = PasswordField("Password", [validators.Length(min=8),validators.Length(max=144)])

    class Meta:
        csrf = False

class LoginForm(FlaskForm):

    username = StringField("Username",[validators.DataRequired()])
    password = PasswordField("Password",[validators.DataRequired()])
    
    class Meta:
        csrf = False