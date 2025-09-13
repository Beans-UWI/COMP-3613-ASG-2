from App.database import db

class Response(db.Model):
    responseId = db.Column(db.Integer, primary_key=True)
    shortlistId = db.Column(db.Integer, db.ForeignKey('shortlist.shortlistId'), nullable=False)
    employerId = db.Column(db.Integer, db.ForeignKey('employer.employerId'), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    # Composition: references to Shortlist and Employer objects
    shortlist = db.relationship('Shortlist', backref='responses')
    employer = db.relationship('Employer', backref='responses')
