from application import db


class Score(db.Model):

    scores_id = db.Column(db.Integer, primary_key=True)
    matches_id = db.Column(db.Integer, db.ForeignKey('match.matches_id'))
    husers_score = db.Column(db.Integer)
    vusers_score = db.Column(db.Integer)


    def __init__(self,matches_id,husers_score,vusers_score):
      self.matches_id = matches_id
      self.husers_score = husers_score
      self.vusers_score = vusers_score