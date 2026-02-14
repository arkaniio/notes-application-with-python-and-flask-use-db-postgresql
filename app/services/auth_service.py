from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token

def register_user(input_username, input_email, input_password):
    
    try: 
        #filter the username and email to make sure that username and email has been already exists!
        if User.query.filter((User.email == input_email) | (User.username == input_username)).first():
            return None, "Email or username has been already exists!"
        
        #define the user input for the form register
        new_user = User(username=input_username, email=input_email, password=input_password)
        new_user.set_password(input_password)

        #add the user using query add
        db.session.add(new_user)
        db.session.commit()

        return new_user.to_Json(), "Register has been successfully"

    except Exception as e:
        db.session.rollback()
        return None, f"The register was not successfully {e}"
    
def login_user(input_username, input_password):
        
    try:

        #filter the user that wants to compare the username in input and in db
        user = User.query.filter(User.username == input_username).first()

        if not user :
            return None, "User was not detected, please try again later !"
        
        if not user.check_password(input_password):
            return None, "Cannot compare the password !"

        #create the token of the user
        token_user = create_access_token(identity=str(user.id))

        #checking or validate the token of the user
        if not token_user:
            return None, "Failed to access and create some token for the user!"

        return user, token_user, "Login as a user has been successfully!"
    
    except Exception as e:
        return None, f"Cannot login as a user ! {e}"
