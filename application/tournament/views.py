from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

import math
from application import app, db
from application.tournament.models import Tournament
from application.match.models import Match
from application.match.views import delete_all_matches
from application.score.views import delete_scores
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
    ).order_by(
        Users_to_tournaments.sort_order,Users.name
    ).all()

    return u_to_t

def user_is_in(tournament_id):

    if not current_user.is_authenticated:
        return False
    
    userin = False
    for user in get_users_to_tournaments(tournament_id):
        if current_user.users_id == user.Users.users_id:
            userin = True
    return userin

def get_user_id(users,sort_order):
    user_id = 0
    for user in users:
        if user.Users_to_tournaments.sort_order == sort_order:
            user_id = user.Users.users_id
    return user_id

def get_sort_order(users,user):
    sort_order = 0
    for user in users:
        if user.Users_to_tournaments.user_id == user:
            user_id = user.Users.sort_order
    return sort_order

def get_count(q):
    count_q = q.statement.with_only_columns([db.func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count

def generate_brackets_se(tournament_id):

    #Single elimination bracket generation

    users = get_users_to_tournaments(tournament_id)
    no_users = len(users)
    no_rounds = math.ceil(math.log2(no_users))
    
    match_no = 1
    matches = []


    luku3 = 0
    for round in range(0,no_rounds):
        r_pow = (2**(no_rounds - round))
        
        luku = 0
        luku2 = 0
        
        for match in range(0,int(r_pow/2)):

            # ugly but works(i hope) :DD

            if round == 0:
                m = Match(match_no,tournament_id,round+1)

                m.husers_id = get_user_id(users,(match + 1))
                m.vusers_id = get_user_id(users,(r_pow - (match)))

                if no_rounds>1:
                    if ((r_pow/2) + luku) < ((r_pow/2)+ ((2**(no_rounds - round - 2)))):
                        luku += 1
                        m.parent_id = int((r_pow/2) + luku)
                    else:
                        m.parent_id = int((r_pow/2)+((2**(no_rounds - round - 2))) - luku2)
                        luku2 += 1
                
            else:
                m = Match(match_no,tournament_id,round+1)
                if round < no_rounds-1:
                    if ((r_pow/2) + luku) < ((r_pow/2)+ ((2**(no_rounds - round - 2)))):
                        luku += 1
                        m.parent_id = int(luku3+(r_pow/2) + luku)
                    else:
                        m.parent_id = int(luku3+(r_pow/2)+((2**(no_rounds - round - 2))) - luku2)
                        luku2 += 1
            
            matches.append(m)
            
            
            match_no += 1
        luku3 = match_no-1

    for m in matches:
        if m.vusers_id == 0:
            hae = m.parent_id
            m.winner = 1
            for mm in matches:
                if mm.match_no == m.parent_id:
                    mm.husers_id = m.husers_id

    for m in matches:
        db.session().add(m)
        db.session().commit()



@app.route("/tournament/new/")
@login_required
def tournament_form():
    return render_template("tournament/new.html", form = TournamentForm())

  
@app.route("/tournament/edit/<tournament_id>/", methods=["POST"])
@login_required
def tournament_edit(tournament_id):

    form = TournamentForm(request.form)
    t = Tournament.query.get(tournament_id)

    

    if not t.owner == current_user.users_id:
        return render_template("index.html", tournaments = Tournament.query.all(), users = Users.count_active_users(),
                               error = "Invalid permissions. This incident will be reported.")

    if not form.validate():
        return render_template("/tournament/edit.html", form = form, error = form.errors)

    t.name = form.name.data
    t.description = form.description.data

    db.session.commit()

    return redirect(url_for("index"))

@app.route("/tournament/start/<tournament_id>/", methods=["GET"])
@login_required
def tournament_start(tournament_id):

    t = Tournament.query.get(tournament_id)

    if not t.owner == current_user.users_id:
        return render_template("index.html", tournaments = Tournament.query.all(), users = Users.count_active_users(), error = "Invalid permissions. This incident will be reported.")

    ttu = db.session.query(Users_to_tournaments).filter(Users_to_tournaments.tournament_id == tournament_id)
    
    if get_count(ttu) < 2:
       return render_template("index.html", tournaments = Tournament.query.all(), users = Users.count_active_users(), error = "Unable to start tournament due to insufficent user count. You need atleast 2 users to start a tournament!")

    t.status = 1
    db.session.commit()

    generate_brackets_se(tournament_id)

    return redirect(url_for("index"))

@app.route("/tournament/stop/<tournament_id>/", methods=["GET"])
@login_required
def tournament_stop(tournament_id):

    t = Tournament.query.get(tournament_id)

    if not t.owner == current_user.users_id:
        return render_template("index.html", tournaments = Tournament.query.all(), users = Users.count_active_users(), error = "Invalid permissions. This incident will be reported.")

    delete_scores(tournament_id)
    delete_all_matches(tournament_id)
    t.status = 0
    db.session.commit()


    return redirect(url_for("index"))

@app.route("/tournament/view/<tournament_id>/", methods=["GET"])
def tournament_view(tournament_id):

    t = Tournament.query.get(tournament_id) 
    m = Match.query.filter(tournament_id==tournament_id).order_by(Match.match_no)

    db.session.commit()

    return render_template("tournament/view.html", tournament = t, users = get_users_to_tournaments(tournament_id), userin = user_is_in(tournament_id), matches = m)

@app.route("/tournament/edit/<tournament_id>/")
@login_required
def tournament_edit_form(tournament_id):

    t = Tournament.query.get(tournament_id)

    if not t.owner == current_user.users_id:
        return render_template("index.html", tournaments = Tournament.query.all(), users = Users.count_active_users(), error = "Invalid permissions. This incident will be reported.")
  
    return render_template("tournament/edit.html", form = TournamentForm(), tournament = t)

@app.route("/tournament/delete/<tournament_id>/", methods=["GET"])
@login_required
def tournament_delete(tournament_id):

    t = Tournament.query.get(tournament_id)

    if not t.owner == current_user.users_id or t.status != 0:
        return render_template("index.html", tournaments = Tournament.query.all(), users = Users.count_active_users(), error = "Invalid permissions. This incident will be reported.")
    
    Users_to_tournaments.query.filter(Users_to_tournaments.tournament_id == tournament_id).delete()
    Tournament.query.filter(Tournament.tournament_id == tournament_id and Tournament.owner == current_user.users_id).delete()
    db.session().commit()

    
    delete_scores(tournament_id)
    delete_all_matches(tournament_id)
  
    return redirect(url_for("index"))

  
@app.route("/tournament/new/", methods=["POST"])
@login_required
def tournament_create():
    form = TournamentForm(request.form)
  
    if not form.validate():
        return render_template("/tournament/new.html", form = form, error = form.errors)
  
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
        return render_template("tournament/view.html", tournament = t, users = get_users_to_tournaments(tournament_id), userin = user_is_in(tournament_id)) #return if user has already joined
    
    max_order = db.session.query(db.func.max(Users_to_tournaments.sort_order))
    max_order = max_order.filter(Users_to_tournaments.tournament_id == tournament_id).scalar() or 0

    lisays = Users_to_tournaments(tournament_id,current_user.users_id,max_order+1)

    db.session().add(lisays)
    db.session().commit()
  
    return render_template("tournament/view.html", tournament = t, users = get_users_to_tournaments(tournament_id), userin = user_is_in(tournament_id))

@app.route("/tournament/part/<tournament_id>/", methods=["GET"])
@login_required
def tournament_part(tournament_id):

    t = Tournament.query.get(tournament_id)
    u = db.session.query(Users)
    ttu = db.session.query(Users_to_tournaments)

    user = db.session().query(Users_to_tournaments).filter(Users_to_tournaments.tournament_id == tournament_id, Users_to_tournaments.user_id == current_user.users_id).first()

    db.session().query(Users_to_tournaments).filter(Users_to_tournaments.tournament_id == tournament_id,Users_to_tournaments.sort_order > user.sort_order).update({Users_to_tournaments.sort_order : Users_to_tournaments.sort_order-1})
    db.session().commit()

    Users_to_tournaments.query.filter(Users_to_tournaments.tournament_id == tournament_id, Users_to_tournaments.user_id == current_user.users_id).delete()
    db.session().commit()
  
    return render_template("tournament/view.html", tournament = t, users = get_users_to_tournaments(tournament_id), userin = user_is_in(tournament_id))