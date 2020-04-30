from flask import Flask, render_template
from application import app
from application.tournament.models import Tournament
from application.login.models import Users

@app.context_processor
def context_processor():
    return dict(key='kek',stats=Users.get_wins())


@app.route("/")
def index():
    return render_template("index.html", tournaments = Tournament.query.all(), users = Users.count_active_users())
