from functools import wraps
from App.controllers.state import *

def require_user_type(required_type): # a factory for the decorator
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            state = get_session_state()
            if not state.logged_in or state.user_type != required_type:
                print(f"Access denied: You must be logged in as {required_type} to use this command.")
                return
            return f(*args, **kwargs)
        return wrapper
    return decorator

# since this is a bit more of an advanced course, 
# I'll start doing advanced stuff i wanted to try, so new design pattern i want to learn being decorators

# so this decorator will check if the user is logged in and if they are the correct user type
# if not, it will print an error message and return without calling the function

# and to show i know why its used, a decorator just extends the functionality of a object without modifying it
# in this case im using it to extend in a cleaner way a check for user type and logged in status, before the function
# that is attached to the cli command is called