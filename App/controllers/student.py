from App.models import Student
from App.database import db

def create_student(username, password, major):
    new_student = Student(username=username, password=password, major=major)
    db.session.add(new_student)
    db.session.commit()
    return new_student

def get_student_by_username(username):
    return db.session.execute(db.select(Student).filter_by(username=username)).scalar_one_or_none()

def get_student_by_id(student_id):
    return db.session.get(Student, student_id)

def can_student_login(username, password):
    student = get_student_by_username(username)
    if not student:
        print("Username not found")
        return False
    if student.password != password:
        print("Incorrect password")
        return False
    print("Student login successful")
    return True