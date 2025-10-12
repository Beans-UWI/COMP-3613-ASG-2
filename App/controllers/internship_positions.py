from App.models import InternshipPositions
from App.database import db
from App.controllers.employer import get_current_employer_id

def create_internship_position(title, description, location, duration, salary, employer_id=None):
    internship = InternshipPositions(
        title=title,
        description=description,
        location=location,
        durationInMonths=duration,
        salary=salary,
        employerId= employer_id if employer_id is not None else get_current_employer_id()
    )
    db.session.add(internship)
    db.session.commit()
    return internship

def get_internship_details(internship_id):
    return db.session.get(InternshipPositions, internship_id)

def get_internships_by_employer_id(employer_id):
    return db.session.execute(db.select(InternshipPositions).filter_by(employerId=employer_id)).scalars().all()

def get_all_internships():
    return db.session.execute(db.select(InternshipPositions)).scalars().all()

def view_all_internships():
    internships = get_all_internships()
    return [i.get_json() for i in internships]