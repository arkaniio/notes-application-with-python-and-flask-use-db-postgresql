from app import db
from app.models.user import User
from flask import jsonify

def register_user(input_username, input_email, input_password):
    
    try: 

        #filter the username and email to make sure that username and email has been already exists!
        if User.query.filter((User.email == input_email) | (User.username == input_username)).first():
            return None, "Email or username has been already exists!"
        
        #define the user input for the form register
        new_user = User(input_username, input_email)
        new_user.set_password(input_password)

        db.session.add(new_user)
        db.session.commit()

        return new_user, "Register has been successfully"

    except Exception as e:
        db.session.rollback()
        return None, f"The register was not successfully {e}"
