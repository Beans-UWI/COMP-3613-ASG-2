import os, tempfile, pytest, logging, unittest
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Staff, InternshipPositions, Shortlist, Employer, Response
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    get_student_by_username,
    get_staff_by_username,
    get_employer_by_username,
    update_user,
    get_internships_by_employer_id,
    create_internship_position,
    create_employer,
    create_student,
    create_staff,
    create_response,
    update_response,
    get_shortlists_by_student_id,
    get_response_by_shortlist_id,
    create_shortlist,
    get_shortlists_by_internship_id,
    get_all_internships,
    get_internship_details,
    can_employer_login,
    can_student_login,
    can_staff_login
    )


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password)
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)


class StudentUnitTests(unittest.TestCase):

    def test_new_student(self):
        new_student = Student(username="john_doe", password="testpass", major="Computer Science")
        assert new_student.username == "john_doe"
    
    def test_student_get_json(self):
        new_student = Student(username="john_doe", password="testpass", major="Computer Science")
        student_json = new_student.get_json()
        expected_json = {
            "studentId": None,
            "username": "john_doe",
            "major": "Computer Science"
        }
        self.assertDictEqual(student_json, expected_json)

class EmployerUnitTests(unittest.TestCase):

    def test_new_employer(self):
        new_employer = Employer(username="emp1", password="testpass", companyName="TechCorp", jobTitle="HR Manager")
        assert new_employer.username == "emp1"

    def test_employer_get_json(self):
        new_employer = Employer(username="emp1", password="testpass", companyName="TechCorp", jobTitle="HR Manager")
        employer_json = new_employer.get_json()
        expected_json = {
            "employerId": None,
            "username": "emp1",
            "companyName": "TechCorp",
            "jobTitle": "HR Manager"
        }
        self.assertDictEqual(employer_json, expected_json)


class StaffUnitTests(unittest.TestCase):

    def test_new_staff(self):
        new_staff = Staff(username="jane_doe", password="testpass", department="DCIT")
        assert new_staff.username == "jane_doe"

    def test_staff_get_json(self):
        staff = Staff("jane_doe", "janepass", "DCIT")
        staff_json = staff.get_json()
        self.assertDictEqual(staff_json, {"staffId":None, "username":"jane_doe", "department":"DCIT"})

class InternshipPositionsUnitTests(unittest.TestCase):
    
    def test_new_internship_position(self):
        internship = InternshipPositions(title="Software Developer", 
                                         description = "Fullstack developer with expertise in cloud", 
                                         location = "San Fernando", 
                                         durationInMonths=3, 
                                         salary = 3000, 
                                         employerId= 1)
        assert internship.title == "Software Developer"
        assert internship.location == "San Fernando"
        assert internship.salary == 3000
        assert internship.description == "Fullstack developer with expertise in cloud"
        assert internship.durationInMonths == 3
        assert internship.employerId == 1
    
    def test_internship_get_json(self):
        internship = InternshipPositions(title="Software Developer", 
                                         description = "Fullstack developer with expertise in cloud", 
                                         location = "San Fernando", 
                                         durationInMonths=3, 
                                         salary = 3000, 
                                         employerId= 1,
                                         createdAt= date.today() )
        internship_json = internship.get_json()
        test_json = {"internshipId": None,
                     "employerId": 1,
                     "title": "Software Developer",
                     "description": "Fullstack developer with expertise in cloud", 
                     "location" : "San Fernando", 
                     "durationInMonths": 3, 
                     "salary": 3000,
                     "createdAt": date.today().isoformat()}
        self.assertDictEqual(internship_json, test_json)

class ShortlistUnitTests(unittest.TestCase):
    
    def test_new_shortlist(self):
        new_shortlist = Shortlist(studentId=1, internshipId=1, staffId=1, lastUpdated=date.today())
        assert new_shortlist.studentId == 1
        assert new_shortlist.staffId == 1
        assert new_shortlist.internshipId == 1
        assert new_shortlist.lastUpdated == date.today()
    
    def test_shortlist_get_json(self):
        new_shortlist = Shortlist(studentId=1, internshipId=1, staffId=1, lastUpdated=date.today())
        shortlist_json = new_shortlist.get_json()
        test_json = { "shortlistId": None, "studentId": 1, "internshipId": 1, "staffId": 1, "lastUpdated": date.today().isoformat() }
        self.assertDictEqual(shortlist_json, test_json)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


class StudentIntegrationTests(unittest.TestCase):
    
    def test_student_login_validation(self):
        student = create_student("phil", "philpass", "Computer Science")
        assert can_student_login("phil", "philpass") == True
        assert can_student_login("phil", "wrongpass") == False
        assert can_student_login("nonexistent", "philpass") == False

    def test_create_student(self):
        student = create_student("alice", "alicepass", "Information Technology")
        assert student.username == "alice"
        assert student.major == "Information Technology"
        assert student.studentId is not None

        retrieved_student = get_student_by_username("alice")
        assert retrieved_student is not None
        assert retrieved_student.studentId == student.studentId


class EmployerIntegrationTests(unittest.TestCase):
    
    def test_employer_login_validation(self):
        employer = create_employer("walter", "walterpass", "ZS Associates", "Recruiter II")
        assert can_employer_login("walter", "walterpass") == True
        assert can_employer_login("walter", "wrongpass") == False
        assert can_employer_login("nonexistent", "walterpass") == False

    def test_create_employer(self):
        employer = create_employer("charles", "charlespass", "Google", "Software Engineer")
        assert employer.username == "charles"
        assert employer.companyName == "Google"
        assert employer.jobTitle == "Software Engineer"
        assert employer.employerId is not None
    
        retrieved_employer = get_employer_by_username("charles")
        assert retrieved_employer is not None
        assert retrieved_employer.employerId == employer.employerId


class StaffIntegrationTests(unittest.TestCase):
    
    def test_staff_login_validation(self):
        staff = create_staff("randy", "randypass", "DCIT")
        assert can_staff_login("randy", "randypass") == True
        assert can_staff_login("randy", "wrongpass") == False
        assert can_staff_login("nonexistent", "randypass") == False

    def test_create_staff(self):
        staff = create_staff("diana", "dianapass", "Engineering")
        assert staff.username == "diana"
        assert staff.department == "Engineering"
        assert staff.staffId is not None

        retrieved_staff = get_staff_by_username("diana")
        assert retrieved_staff is not None
        assert retrieved_staff.staffId == staff.staffId


class InternshipIntegrationTests(unittest.TestCase):

    def test_create_internship_position(self):
        employer = create_employer("eva", "evapass", "Amazon", "Tech Lead")
        internship = create_internship_position(
            title="Data Scientist", 
            description="Data scientist with expertise in machine learning", 
            location="Los Angeles", 
            duration=6, 
            salary=5000, 
            employer_id=employer.employerId
        )
        
        assert internship.title == "Data Scientist"
        assert internship.description == "Data scientist with expertise in machine learning"
        assert internship.location == "Los Angeles"
        assert internship.durationInMonths == 6
        assert internship.salary == 5000
        assert internship.employerId == employer.employerId
        assert internship.internshipId is not None
        
        retrieved_internship = get_internship_details(internship.internshipId)
        assert retrieved_internship is not None
        assert retrieved_internship.title == "Data Scientist"
        
        assert internship.employer is not None
        assert internship.employer.employerId == employer.employerId
    
    def test_get_internships_by_employer(self):
        employer = create_employer("bill", "billpass", "Davyn", "Senior Engineer")
        internship1 = create_internship_position(title="Software Developer", 
                                         description = "Fullstack engineer with expertise in cloud", 
                                         location = "San Fernando", 
                                         duration=3, 
                                         salary = 3000, 
                                         employer_id= 1)
        internship2 = create_internship_position(title="Software Engineer", 
                                         description = "Fullstack engineer with expertise in python", 
                                         location = "San Fernando", 
                                         duration=12, 
                                         salary = 4000, 
                                         employer_id= 1)
        employers_internships = get_internships_by_employer_id(1)
        temp_internships = InternshipPositions.query.filter_by(employerId=1).all()
        assert employers_internships == temp_internships
    
    def test_get_all_internships(self):
        employer = create_employer("carol", "carolpass", "Meta", "Product Manager")
        internship1 = create_internship_position(
            title="Backend Developer", 
            description="Backend developer with expertise in databases", 
            location="New York", 
            duration=4, 
            salary=3500, 
            employer_id=employer.employerId
        )
        internship2 = create_internship_position(
            title="Frontend Developer", 
            description="Frontend developer with expertise in React", 
            location="New York", 
            duration=5, 
            salary=3200, 
            employer_id=employer.employerId
        )
        
        all_internships = get_all_internships()
        assert len(all_internships) >= 2
        assert internship1 in all_internships
        assert internship2 in all_internships

class ShortlistIntegrationTests(unittest.TestCase):
    
    def test_create_shortlist(self):
        student = create_student("mike", "mikepass", "Software Engineering")
        employer = create_employer("company", "pass", "Company", "Manager")
        staff = create_staff("sara", "sarapass", "DCIT")
        internship = create_internship_position(
            title="Test Internship",
            description="Test description",
            location="Test Location",
            duration=3,
            salary=3000,
            employer_id=employer.employerId
        )
        
        shortlist = create_shortlist(
            student_id=student.studentId,
            internship_id=internship.internshipId,
            staff_id=staff.staffId
        )
        
        assert shortlist.studentId == student.studentId
        assert shortlist.internshipId == internship.internshipId
        assert shortlist.staffId == staff.staffId
        assert shortlist.shortlistId is not None
        
        temp_shortlist = get_shortlists_by_internship_id(internship.internshipId)[0]
        assert shortlist == temp_shortlist
    
    def test_get_shortlist_by_student(self):
        student = create_student("john", "johnpass", "Computer Science")
        staff = create_staff("pam", "pampass", "DCIT")
        shortlist1 = create_shortlist(student_id=1, internship_id=1, staff_id=1)
        shortlist2 = create_shortlist(student_id=1, internship_id=2, staff_id=1)
        student_shortlists = get_shortlists_by_student_id(1)
        assert student_shortlists == [shortlist1, shortlist2]

    def test_get_shortlist_by_student(self):
        student = create_student("harry", "harrypass", "Information Technology")
        shortlist1 = create_shortlist(student_id=2, internship_id=1, staff_id=1)
        shortlists = get_shortlists_by_internship_id(1)
        temp_shortlists = Shortlist.query.filter_by(internshipId=1).all()
        assert shortlists == temp_shortlists

class ResponseIntegrationTests(unittest.TestCase):
    
    def test_create_response(self):
        new_response = create_response(shortlist_id=1, employer_id=1, status="Pending")
        temp_response = get_response_by_shortlist_id(1)
        assert new_response == temp_response

    def test_update_response(self):
        new_response = create_response(1, 1, "Accepted")
        response = get_response_by_shortlist_id(1)
        update_response(response.responseId, "rejected")
        updated_response = get_response_by_shortlist_id(1)
        assert updated_response.status == "rejected"
