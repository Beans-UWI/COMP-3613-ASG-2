from App.database import db

class Staff(db.Model):
    staffId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    
    def get_json(self):
        return {
            'staffId': self.staffId,
            'username': self.username,
            'department': self.department
        }