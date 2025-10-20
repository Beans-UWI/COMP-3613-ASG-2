from App.models import Staff
from App.controllers.state import get_session_state
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
    if not staff.check_password(password):
        print("Incorrect password")
        return False
    print("Staff login successful")
    return True

def get_current_staff_id():
    state = get_session_state()
    username = state.username
    staff = get_staff_by_username(username)
    if staff:
        return staff.staffId
    return None