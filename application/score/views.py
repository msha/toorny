from application import app, db

from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application.match.models import Match
from application.match.views import match_view
from application.login.models import Users
from application.score.models import Score
from application.users_to_tournaments.models import Users_to_tournaments
from application.tournament.models import Tournament

from application.match.forms import ScoreForm,SelectWinner

@app.route("/match/scores/<match_id>/", methods=["POST"])
@login_required
def post_score(match_id):

    form = ScoreForm(request.form)

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
    
    if not form.validate():
      return match_view(match_id)

    if not (current_user.users_id == t.owner or current_user.users_id in ids):
        return render_template("index.html",
                               error = "Invalid permissions. This incident will be reported.")


    s = Score(m.matches_id,request.form.get("home_score"),request.form.get("visitor_score"))
    
    db.session.add(s)
    db.session.commit()

    return match_view(match_id)

@app.route("/match/scores/del/<scores_id>/", methods=["GET"])
@login_required
def delete_score(scores_id):
  s = Score.query.get(scores_id)
  match_id = s.matches_id
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

  ids = []
  for user in u:
      ids.append(user.Users.users_id)

  if not (current_user.users_id == t.owner or current_user.users_id in ids):
        return render_template("index.html",
                               error = "Invalid permissions. This incident will be reported.")

  Score.query.filter(Score.scores_id == scores_id).delete()
  db.session().commit()

  return match_view(match_id)

def delete_scores(tournament_id):
  m = db.session.query(Match).filter(Match.tournament_id == tournament_id).all()
  for match in m:
    Score.query.filter(Score.matches_id == match.matches_id).delete()