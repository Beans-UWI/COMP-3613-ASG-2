import os, tempfile, pytest, logging, unittest
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Staff, InternshipPositions, Shortlist
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
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
        

