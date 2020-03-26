from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application.login.models import Users
from application.login.forms import RegisterForm
from application.login.forms import LoginForm

@app.route("/register/")
def register_form():
    return render_template("login/register.html", form = RegisterForm())

@app.route("/register/", methods=["POST"])
def registration():

    form = RegisterForm(request.form)

    u = Users(request.form.get("name"),request.form.get("username"),request.form.get("password"))

    if not form.validate():
        return render_template("login/register.html", form = form)

    db.session().add(u)
    db.session().commit()
  
    return redirect(url_for("index"))

@app.route("/users", methods=["GET"])
def users():
    return render_template("index")

@app.route("/users/<users_id>/", methods=["POST"])
def users_ban(users_id):

    u = Users.query.get(users_id)
    u.banned = True
    db.session().commit()
  
    return redirect(url_for("users"))

@app.route("/login", methods = ["GET", "POST"])
def login_form():
    if request.method == "GET":
        return render_template("login/login.html", form = LoginForm())

    form = LoginForm(request.form)

    user = Users.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("login/login.html", form = form,
                               error = "No such username or password")

    login_user(user)
    print("Welcome " + user.name + "!")
    return redirect(url_for("index"))    

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))   