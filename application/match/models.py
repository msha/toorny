from application import db


class Match(db.Model):

    matches_id = db.Column(db.Integer, primary_key=True)
    Tournaments_id = db.Column(db.Integer, db.ForeignKey('tournament.tournament_id'),
                               nullable=False)
    HUsers_id = db.Column(db.Integer, db.ForeignKey('users.users_id'),
                          nullable=False)
    VUsers_id = db.Column(db.Integer,
                          nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name
