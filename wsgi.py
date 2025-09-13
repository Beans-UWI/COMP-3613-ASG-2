import click, pytest, sys
from flask.cli import AppGroup

from App.database import db, get_migrate
from App.models import * # im aware import all is not best practice but its a cli simulation and itll make things easier
from App.controllers import *
from App.utils.user_type_decorator import require_user_type
from App.main import create_app
from App.controllers import ( initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# login command
login_cli = AppGroup('login', help='User management commands')

@login_cli.command("user-login", help="Log in a user")
@click.argument("user-type")
@click.argument("username")
@click.argument("password")
def login_user_command(user_type, username, password):
    match (user_type): #why python have to be weird and not just name it switch
        case "staff":
            logout_session()
            if can_staff_login(username, password):
                login_session(username, user_type)
        case "student":
            logout_session()
            if can_student_login(username, password):
                login_session(username, user_type)
        case "employer":
            logout_session()
            if can_employer_login(username, password):
                login_session(username, user_type)
    print(f'Logged in {user_type} - {username}...')
    
app.cli.add_command(login_cli)

# logout command
logout_cli = AppGroup('logout', help='User management commands')

@logout_cli.command("user-logout", help="Log out the current user")
def logout_user_command():
    logout_session()
    print('Logged out successfully.')
    
app.cli.add_command(logout_cli)

#staff commands
staff_cli = AppGroup('staff', help='Staff user commands')

@staff_cli.command("list-internships", help="List all internships")
@require_user_type("staff")
def list_internships_command():
    print("Listing all internships...")
    # call a controller function to get internships from the database

@staff_cli.command("add-student", help="Add a student to internship shortlist")
@click.argument("student_id")
@click.argument("internship_id")
def add_student_command(student_id, internship_id):
    print(f"Adding student {student_id} to internship {internship_id} shortlist...")

app.cli.add_command(staff_cli)

# employer commands
employer_cli = AppGroup('employer', help='Employer user commands')
@employer_cli.command("create-internship", help="Create a new internship")
def create_internship_command():
    print("Creating a new internship...")
    #controller function to create a new internship
@employer_cli.command("view-shortlist", help="View applications for an internship")
@click.argument("internship_id")
def view_shortlist_command(internship_id):
    print(f"Viewing internship shortlist for internship {internship_id}...")
    #controller function to view internship shortlist
@employer_cli.command("accept-student", help="Accept a student for an internship")
@click.argument("student_id")
@click.argument("internship_id")
def accept_student_command(student_id, internship_id):
    print(f"Accepting student {student_id} for internship {internship_id}...")
    #controller function to accept a student for an internship
@employer_cli.command("reject-student", help="Reject a student for an internship")
@click.argument("student_id")
@click.argument("internship_id")
def reject_student_command(student_id, internship_id):
    print(f"Rejecting student {student_id} for internship {internship_id}...")
    #controller function to reject a student for an internship

app.cli.add_command(employer_cli)

# student commands
student_cli = AppGroup('student', help='Student user commands')
@student_cli.command("list-shortlist", help="List shortlisted internships")
def list_shortlisted_internships_command():
    print("Listing shortlisted internships...")
    #controller function to list shortlisted internships
@student_cli.command("view-employer-response", help="View employer response for an internship")
@click.argument("internship_id")
def view_employer_command(internship_id):
    print(f"Viewing employer response for internship {internship_id}...")
    #controller function to view employer response for an internship
app.cli.add_command(student_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)