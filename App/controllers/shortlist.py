from App.models import Shortlist
from App.controllers import get_employer_by_id, get_internships_by_employer_id, get_student_by_id
from App.controllers.state import get_session_state
from App.controllers.staff import get_current_staff_id
from App.database import db

def create_shortlist(student_id, internship_id, staff_id=None):
    staff_id = staff_id if staff_id is not None else get_current_staff_id()
    if not staff_id:
        raise ValueError("No staff member is currently logged in.")
    new_shortlist = Shortlist(studentId=student_id, internshipId=internship_id, staffId=staff_id, lastUpdated=db.func.current_timestamp())
    db.session.add(new_shortlist)
    db.session.commit()
    return new_shortlist

def get_shortlist_by_id(shortlist_id):
    return db.session.get(Shortlist, shortlist_id)

def get_shortlists_by_student_id(student_id):
    return db.session.execute(db.select(Shortlist).filter_by(studentId=student_id)).scalars().all()

def get_shortlists_by_internship_id(internship_id):
    if isinstance(internship_id, int):
        return Shortlist.query.filter_by(internshipId=internship_id).all()
    elif isinstance(internship_id, list):
        return Shortlist.query.filter(Shortlist.internshipId.in_(internship_id)).all()


# this was way more annoying than i thought it would be
def view_all_shortlists(id=None, user_type=None):
    state = get_session_state()
    user_type = user_type if user_type is not None else state.user_type

    if user_type == "student":
        student = get_student_by_id(id)
        shortlists = get_shortlists_by_student_id(student.studentId)
        return [s.get_json() for s in shortlists]

    elif user_type == "employer":
        employer = get_employer_by_id(id)
        internships = get_internships_by_employer_id(employer.employerId)
        internship_ids = [i.internshipId for i in internships]
        shortlists = get_shortlists_by_internship_id(internship_ids)
        return [s.get_json() for s in shortlists]

    else:
        return []
    
def view_shortlist_by_internship_id(internship_id):
    shortlists = get_shortlists_by_internship_id(internship_id)
    return [s.get_json() for s in shortlists]