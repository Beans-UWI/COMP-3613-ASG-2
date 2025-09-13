from App.models import Employer
from App.database import db

def create_employer(username, password, companyName, jobTitle):
    new_employer = Employer(username=username, password=password, companyName=companyName, jobTitle=jobTitle)
    db.session.add(new_employer)
    db.session.commit()
    return new_employer

def get_employer_by_username(username):
    return db.session.execute(db.select(Employer).filter_by(username=username)).scalar_one_or_none()

def can_employer_login(username, password):
    employer = get_employer_by_username(username)
    if not employer:
        print("Username not found")
        return False
    if employer.password != password:
        print("Incorrect password")
        return False
    print("Employer login successful")
    return True