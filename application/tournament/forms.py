from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,validators

class TournamentForm(FlaskForm):

    name = StringField("Name", [validators.Length(min=5),validators.Length(max=144)])
    description = TextAreaField("Description", [validators.Length(max=5000)])
    type = SelectField(u'Tournament Type', choices=[('1', 'Single Elimination')])

    class Meta:
        csrf = False