from application import db


class Match(db.Model):

    matches_id = db.Column(db.Integer, primary_key=True)
    match_no = db.Column(db.Integer)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.tournament_id'),
                               nullable=False)
    parent_id = db.Column(db.Integer)
    round = db.Column(db.Integer)
    husers_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    vusers_id = db.Column(db.Integer)
    winner = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    Score = db.relationship("Score", backref='Match', lazy=True)

    def __init__(self, match_no, tournament_id,round):
        self.match_no = match_no
        self.tournament_id = tournament_id
        self.round = round
