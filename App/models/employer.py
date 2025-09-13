from App.database import db

class Employer(db.Model):
    employerId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    companyName = db.Column(db.String(100), nullable=False)
    jobTitle = db.Column(db.String(100), nullable=False)