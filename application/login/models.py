from application import db

from sqlalchemy.sql import text

class Users(db.Model):

    users_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    name = db.Column(db.String(144), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    user_group = db.Column(db.Integer, nullable=False)

    Tournaments = db.relationship("Tournament", backref='Users', lazy=True)
    Users_to_tournaments = db.relationship("Users_to_tournaments", backref='Users', lazy=True)
    Matches = db.relationship("Match", backref='Users', lazy=True)

    def __init__(self, name, username, password):
        self.username = username
        self.name = name
        self.password = password
        self.user_group = 1

    def get_id(self):
        return self.users_id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def count_users():
        stmt = text("SELECT count(*) FROM users")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response = row[0]

        return response

    @staticmethod
    def count_active_users():
        stmt = text("SELECT count(*) FROM users "
                    "where users_id in "
                    "(select users_id from users_to_tournaments)")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response = row[0]

        return response