from application import db

class Match(db.Model):

    
    matches_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)


    def __init__(self, name) :
        self.name = name
    