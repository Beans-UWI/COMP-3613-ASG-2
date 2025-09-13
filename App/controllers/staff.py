from App.models import Staff
from App.database import db

def create_staff(username, password, department):
    new_staff = Staff(username=username, password=password, department=department)
    db.session.add(new_staff)
    db.session.commit()
    return new_staff

def get_staff_by_username(username):
    return db.session.execute(db.select(Staff).filter_by(username=username)).scalar_one_or_none()

def can_staff_login(username, password):
    staff = get_staff_by_username(username)
    if not staff:
        print("Username not found")
        return False
    if staff.password != password:
        print("Incorrect password")
        return False
    print("Staff login successful")
    return True