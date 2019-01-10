from rest_api_oscar.database import db

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date_established = db.Column(db.DateTime)
    
    def __init__(self, id, name,  date_established=None):
        self.name = name
        self.date_established = date_established
        self.id=id