from application import db

class Users_to_tournaments(db.Model):
    
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.tournament_id'),
                           nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'),
                           nullable=False)
    sort_order = db.Column(db.Integer)
    
    __table_args__ = (db.PrimaryKeyConstraint('tournament_id', 'user_id'),
                     )
    

    def __init__(self, tournament_id, user_id,sort_order) :
        self.tournament_id = tournament_id
        self.user_id = user_id
        self.sort_order = sort_order