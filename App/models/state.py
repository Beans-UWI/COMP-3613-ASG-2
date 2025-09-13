from App.database import db

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=1)
    username = db.Column(db.String(50), nullable=True)
    user_type = db.Column(db.String(20), nullable=True)
    logged_in = db.Column(db.Boolean, default=False)

    def get_json(self): # returns the state of the user session as a JSON object, if i need it
        return {
            "username": self.username,
            "user_type": self.user_type,
            "logged_in": self.logged_in
        }