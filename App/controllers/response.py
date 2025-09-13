from App.controllers.employer import get_current_employer_id
from App.models import Response
from App.database import db

def create_response(shortlist_id, employer_id, status):
    existing_response = get_response_by_shortlist_id(shortlist_id)
    
    if existing_response:
        existing_response.status = status
        existing_response.employerId = employer_id
        db.session.commit()
        return existing_response
    else:
        response = Response(shortlistId=shortlist_id, employerId=employer_id, status=status)
        db.session.add(response)
        db.session.commit()
        return response

def get_response_by_shortlist_id(shortlist_id):
    return db.session.execute(db.select(Response).filter_by(shortlistId=shortlist_id)).scalar_one_or_none()

def view_response(shortlist_id):
    response = get_response_by_shortlist_id(shortlist_id)
    return response.get_json() if response else print("No response found")

def accept_student(shortlist_id): 
    create_response(shortlist_id, get_current_employer_id(), "accepted")

def reject_student(shortlist_id):
    create_response(shortlist_id, get_current_employer_id(), "rejected")