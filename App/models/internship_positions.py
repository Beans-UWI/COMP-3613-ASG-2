from App.database import db

class InternshipPositions(db.Model):
    __tablename__ = 'internship_positions'
    internshipId = db.Column(db.Integer, primary_key=True)
    employerId = db.Column(db.Integer, db.ForeignKey('employer.employerId'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Float, nullable=True)
    createdAt = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    
    # Composition: reference to Employer object
    employer = db.relationship('Employer', backref='internship_positions')