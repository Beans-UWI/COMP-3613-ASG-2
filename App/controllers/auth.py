from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User, Student, Employer, Staff
from App.database import db

def login(username, password):
  result = db.session.execute(db.select(User).filter_by(username=username))
  user = result.scalar_one_or_none()
  if user and user.check_password(password):
    return create_access_token(identity=str(user.id), additional_claims={"role": "user", "username": user.username})

  # Student
  result = db.session.execute(db.select(Student).filter_by(username=username))
  student = result.scalar_one_or_none()
  if student and student.check_password(password):
    return create_access_token(identity=str(student.studentId), additional_claims={"role": "student", "username": student.username})

  # Employer
  result = db.session.execute(db.select(Employer).filter_by(username=username))
  employer = result.scalar_one_or_none()
  if employer and employer.check_password(password):
    return create_access_token(identity=str(employer.employerId), additional_claims={"role": "employer", "username": employer.username})

  # Staff
  result = db.session.execute(db.select(Staff).filter_by(username=username))
  staff = result.scalar_one_or_none()
  if staff and staff.check_password(password):
    return create_access_token(identity=str(staff.staffId), additional_claims={"role": "staff", "username": staff.username})

  return None


def setup_jwt(app):
  jwt = JWTManager(app)

  # Always store a string user id in the JWT identity (sub),
  # whether a User object or a raw id is passed.
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    user_id = getattr(identity, "id", identity)
    return str(user_id) if user_id is not None else None

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data.get("sub")
    role = jwt_data.get("role", "user")
    # Cast back to int primary key
    try:
      user_id = int(identity)
    except (TypeError, ValueError):
      return None

    model_map = {
      "user": User,
      "student": Student,
      "employer": Employer,
      "staff": Staff,
    }
    model = model_map.get(role, User)
    return db.session.get(model, user_id)

  return jwt


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          identity = get_jwt_identity()
          user_id = int(identity) if identity is not None else None
          current_user = db.session.get(User, user_id) if user_id is not None else None
          is_authenticated = current_user is not None
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)