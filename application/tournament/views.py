from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.tournament.models import Tournament
from application.tournament.forms import TournamentForm
  
@app.route("/tournament/new/")
@login_required
def tournament_form():
    return render_template("tournament/new.html", form = TournamentForm())

  
@app.route("/tournament/edit/<tournament_id>/", methods=["POST"])
@login_required
def tournament_edit(tournament_id):

    form = TournamentForm(request.form)
    t = Tournament.query.get(tournament_id)
    t.name = form.name.data
    t.description = form.description.data

    db.session.commit()

    return redirect(url_for("index"))

@app.route("/tournament/edit/<tournament_id>/")
@login_required
def tournament_edit_form(tournament_id):

    t = Tournament.query.get(tournament_id)
  
    return render_template("tournament/edit.html", form = TournamentForm(), tournament = t)

@app.route("/tournament/delete/<tournament_id>/", methods=["GET"])
@login_required
def tournament_delete(tournament_id):

    Tournament.query.filter(Tournament.tournament_id == tournament_id and Tournament.owner == current_user.users_id).delete()
    db.session().commit()
  
    return redirect(url_for("index"))

  
@app.route("/tournament/new/", methods=["POST"])
@login_required
def tournament_create():
    form = TournamentForm(request.form)
  
    if not form.validate():
        return render_template("/tournament/new.html", form = form)
  
    t = Tournament(form.name.data,form.description.data,current_user.users_id)
    t.type = form.type.data
  
    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("index"))