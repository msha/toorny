from application import db

class Users(db.Model):
    
    users_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),nullable=False)
    password = db.Column(db.String(144), nullable=False)
    name = db.Column(db.String(144), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    user_group = db.Column(db.Integer, nullable=False)

    tournaments = db.relationship("Tournament", backref='users', lazy=True)

    def __init__(self, name, username, password) :
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