from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.tournament.models import Tournament
from application.users_to_tournaments.models import Users_to_tournaments
from application.login.models import Users
from application.tournament.forms import TournamentForm

def get_users_to_tournaments(tournament_id):
    
    u_to_t = db.session.query(
    Users_to_tournaments,Users
    ).filter(
        Users_to_tournaments.tournament_id==tournament_id,
    ).filter(
            Users.users_id == Users_to_tournaments.user_id
    ).all()

    return u_to_t


  
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

@app.route("/tournament/view/<tournament_id>/", methods=["GET"])
@login_required
def tournament_view(tournament_id):

    t = Tournament.query.get(tournament_id)      

    db.session.commit()

    return render_template("tournament/view.html", tournament = t, users = get_users_to_tournaments(tournament_id))

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

@app.route("/tournament/join/<tournament_id>/", methods=["GET"])
@login_required
def tournament_join(tournament_id):

    t = Tournament.query.get(tournament_id)
    u = db.session.query(Users)
    ttu = db.session.query(Users_to_tournaments)

    if Users_to_tournaments.query.filter(Users_to_tournaments.tournament_id == tournament_id, Users_to_tournaments.user_id == current_user.users_id).count() > 0:
        return render_template("tournament/view.html", tournament = t, users = get_users_to_tournaments(tournament_id)) #return if user has already joined
    
    lisays = Users_to_tournaments(tournament_id,current_user.users_id)

    db.session().add(lisays)
    db.session().commit()
  
    return render_template("tournament/view.html", tournament = t, users = get_users_to_tournaments(tournament_id))

@app.route("/tournament/part/<tournament_id>/", methods=["GET"])
@login_required
def tournament_part(tournament_id):

    t = Tournament.query.get(tournament_id)
    u = db.session.query(Users)
    ttu = db.session.query(Users_to_tournaments)

    Users_to_tournaments.query.filter(Users_to_tournaments.tournament_id == tournament_id, Users_to_tournaments.user_id == current_user.users_id).delete()
    db.session().commit()
  
    return render_template("tournament/view.html", tournament = t, users = get_users_to_tournaments(tournament_id))