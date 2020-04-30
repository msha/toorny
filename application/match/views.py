from application import app, db

from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application.match.models import Match
from application.login.models import Users
from application.score.models import Score
from application.users_to_tournaments.models import Users_to_tournaments
from application.tournament.models import Tournament
from application.match.forms import ScoreForm,SelectWinner

def delete_all_matches(tournament_id):
    Match.query.filter(Match.tournament_id == tournament_id).delete()
    db.session().commit()
  
    return redirect(url_for("index"))

@app.route("/match/view/<match_id>/", methods=["GET"])
def match_view(match_id):

    m = Match.query.get(match_id)
    t = Tournament.query.get(m.tournament_id)
    u = db.session.query(Users,Users_to_tournaments
    ).filter(
        (Users_to_tournaments.tournament_id == m.tournament_id)&((Users_to_tournaments.user_id == m.husers_id))
    ).order_by(
        Users_to_tournaments.sort_order
    ).filter(
        (Users.users_id == m.husers_id) | (Users.users_id == m.vusers_id)
    ).all()
    s = db.session.query(Score
    ).filter(
        Score.matches_id == match_id
    ).all()

    users = []
    for user in u:
        users.append((user.Users.users_id,user.Users.name))

    f = ScoreForm(request.form)
    f2 = SelectWinner(request.form)
    f2.winner.choices = users
    

    return render_template("match/view.html", match = m, users = u, tournament = t, scoreform = f, winform = f2, scores = s)

@app.route("/match/win/<match_id>/", methods=["POST"])
@login_required
def match_win(match_id):

    form = SelectWinner(request.form)

    winner = int(request.form.get('winner'))

    m = Match.query.get(match_id)
    t = Tournament.query.get(m.tournament_id)
    u = db.session.query(Users,Users_to_tournaments
    ).filter(
        (Users_to_tournaments.tournament_id == m.tournament_id)&((Users_to_tournaments.user_id == m.husers_id))
    ).order_by(
        Users_to_tournaments.sort_order
    ).filter(
        (Users.users_id == m.husers_id) | (Users.users_id == m.vusers_id)
    ).all()

    users = []
    ids = []
    for user in u:
        ids.append(user.Users.users_id)
        users.append((user.Users.users_id,user.Users.name))

    if int(winner) not in ids and (current_user.users_id != t.owner or current_user.users_id not in ids):
        return render_template("index.html", tournaments = Tournament.query.all(), users = Users.count_active_users(),
                               error = "Invalid permissions. This incident will be reported.")

    f = ScoreForm(request.form)
    f2 = SelectWinner(request.form)
    f2.winner.choices = users

    if winner == m.husers_id:
        m.winner = 1
    elif winner == m.vusers_id:
        m.winner = 2

    if m.parent_id != None:
        m2 = Match.query.get(m.parent_id)
        if m2.husers_id == None:
            m2.husers_id = winner
        elif m2.vusers_id == None:
            m2.vusers_id = winner
        else: 
            return render_template("index.html",
                                error = "Huppelis keikkaa joku meni pahasti pieleen :D") 
    elif m.parent_id == None:
        t.status = 2

    db.session.commit()

    return render_template("match/view.html", match = m, users = u, tournament = t, scoreform = f, winform = f2)