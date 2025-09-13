from App.database import db

class Student(db.Model):
    studentId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    major = db.Column(db.String(100), nullable=False)