from app.models.user import User
from app.models.user import db

def get_user_byId(user_id):

    try:

        #get the user identity
        user = User.query.get(user_id)

        #validate the user if not exists
        if not user:
            return None, "The user has not exist in db that you want !"
    
        return user, "User has been detected and get successfully!"
    
    except Exception as e:
        return None, f"Failed to get the user ! {e}"