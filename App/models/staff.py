from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash

class Staff(db.Model):
    staffId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password, department):
        self.department = department
        self.set_password(password)
        self.username = username
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def get_json(self):
        return {
            'staffId': self.staffId,
            'username': self.username,
            'department': self.department
        }