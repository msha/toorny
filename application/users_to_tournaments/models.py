from application import db

class Users_to_tournaments(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.tournament_id'),
                           nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'),
                           nullable=False)

    def __init__(self, tournament_id, user_id) :
        self.tournament_id = tournament_id
        self.user_id = user_id