from App.models import Employer
from App.controllers.state import get_session_state
from App.database import db

def create_employer(username, password, companyName, jobTitle):
    new_employer = Employer(username=username, password=password, companyName=companyName, jobTitle=jobTitle)
    db.session.add(new_employer)
    db.session.commit()
    return new_employer

def get_employer_by_username(username):
    return db.session.execute(db.select(Employer).filter_by(username=username)).scalar_one_or_none()

def get_employer_by_id(employer_id):
    return db.session.get(Employer, employer_id)

def can_employer_login(username, password):
    employer = get_employer_by_username(username)
    if not employer:
        print("Username not found")
        return False
    if not employer.check_password(password):
        print("Incorrect password")
        return False
    print("Employer login successful")
    return True

def get_current_employer_id():
    state = get_session_state()
    username = state.username
    employer = get_employer_by_username(username)
    if employer:
        return employer.employerId
    return None