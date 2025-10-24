from .student import create_student
from .employer import create_employer
from .staff import create_staff
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_student("student1", "password1", "Computer Science")
    create_student("student2", "password1", "Computer Science")
    create_employer("employer1", "password1", "Tech Corp", "Software Engineer")
    create_staff("staff1", "password1", "Administration")