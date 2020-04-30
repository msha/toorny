from application import db

from sqlalchemy.sql import text

class Users(db.Model):

    users_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
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
        
    @staticmethod
    def get_wins():
        stmt = text("select u.name, count(*) as wins, (select count(*) from match where (husers_id = u.users_id or vusers_id = u.users_id) and winner > 0) "
                    "from users u "
                    "join users_to_tournaments utt on u.users_id = utt.user_id  "
                    "join tournament t on utt.tournament_id = t.tournament_id  "
                    "join match m on m.tournament_id = t.tournament_id  "
                    "where (u.users_id = m.husers_id and m.winner = 1) or (u.users_id = m.vusers_id and m.winner = 2) "
                    "group by u.users_id "
                    "order by wins desc  "
                    "limit 10 ;")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append((row[0],row[1],row[2]))

        return response