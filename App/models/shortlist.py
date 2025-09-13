from App.database import db

class Shortlist(db.Model):
    shortlistId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('student.studentId'), nullable=False)
    internshipId = db.Column(db.Integer, db.ForeignKey('internship_positions.internshipId'), nullable=False)
    staffId = db.Column(db.Integer, db.ForeignKey('staff.staffId'), nullable=True)
    lastUpdated = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    
    # Composition: references to Student, InternshipPositions, and Staff objects
    student = db.relationship('Student', backref='shortlists')
    internship = db.relationship('InternshipPositions', backref='shortlists')
    staff = db.relationship('Staff', backref='shortlists')