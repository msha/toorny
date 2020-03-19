from application import app, db
from flask import render_template, request, redirect, url_for
from application.login.models import Users

@app.route("/register/")
def register_form():
    return render_template("login/register.html")

@app.route("/register/", methods=["POST"])
def registration():
    u = Users(request.form.get("name"))

    db.session().add(u)
    db.session().commit()
  
    return redirect(url_for("users"))

@app.route("/users", methods=["GET"])
def users():
    return render_template("login/users.html", users = Users.query.all())

@app.route("/users/<users_id>/", methods=["POST"])
def users_ban(users_id):

    u = Users.query.get(users_id)
    u.banned = True
    db.session().commit()
  
    return redirect(url_for("users"))