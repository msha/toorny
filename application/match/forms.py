from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,validators,SelectField,IntegerField

class ScoreForm(FlaskForm):

    home_score = IntegerField("Home_Score",[validators.DataRequired(),validators.NumberRange(0,10000)])
    visitor_score = IntegerField("Visitor_Score",[validators.DataRequired(),validators.NumberRange(0,10000)])
    
    class Meta:
        csrf = False

class SelectWinner(FlaskForm):

    winner = SelectField(u'Winner', choices=[])

    class Meta:
        csrf = False