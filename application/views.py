from flask import Flask, render_template
from application import app
from application.tournament.models import Tournament


@app.route("/")
def index():
    return render_template("index.html", tournaments = Tournament.query.all())
