from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
  app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views

from application.login import models
from application.login import views

from application.tournament import models
from application.tournament import views

from application.match import models
from application.match import views

from application.score import views
from application.score import models

from application.login.models import Users

from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login_form"
login_manager.login_message = "Please login to the service"

@login_manager.user_loader
def load_user(user_id):
  return Users.query.get(user_id)

db.create_all()