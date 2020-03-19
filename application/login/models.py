from application import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    banned = db.Column(db.Boolean, nullable=False)

    def __init__(self, username):
        self.username = username
        self.banned = False