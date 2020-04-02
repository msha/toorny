from application import db

class Tournament(db.Model):
    
    tournament_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144),nullable=False)
    type = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    start_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    end_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Integer, nullable=False)

    owner = db.Column(db.Integer, db.ForeignKey('users.users_id'),
                           nullable=False)

    Match = db.relationship("Match", backref='Tournament', lazy=True)
    Users_to_tournaments = db.relationship("Users_to_tournaments", backref='Tournament', lazy=True)

    def __init__(self, name, description,owner) :
        self.name = name
        self.description = description
        self.status = 0
        self.owner = owner


