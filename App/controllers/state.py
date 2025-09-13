from App.models.state import State
from App.database import db

def get_session_state():
    state = db.session.get(State, 1)
    if not state:
        state = State(id=1)
        db.session.add(state)
        db.session.commit()
    return state

def login_session(username, user_type, logged_in=True):
    state = get_session_state()
    state.username = username
    state.user_type = user_type
    state.logged_in = logged_in
    db.session.commit()

def logout_session():
    state = get_session_state()
    state.username = None
    state.user_type = None
    state.logged_in = False
    db.session.commit()