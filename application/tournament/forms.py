from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,validators

class TournamentForm(FlaskForm):

    name = StringField("Name")
    description = TextAreaField("Description")
    type = SelectField(u'Tournament Type', choices=[('1', 'Single Elimination'), ('2', 'Double Elimination'), ('3', 'Round Robin')])

    class Meta:
        csrf = False