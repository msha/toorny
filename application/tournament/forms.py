from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,validators

class TournamentForm(FlaskForm):

    name = StringField("Name", [validators.Length(min=5),validators.Length(max=144)])
    description = TextAreaField("Description", [validators.Length(max=500)])
    type = SelectField(u'Tournament Type', choices=[('1', 'Single Elimination'), ('2', 'Double Elimination'), ('3', 'Round Robin')])

    class Meta:
        csrf = False