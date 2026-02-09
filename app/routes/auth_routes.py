from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user
from app.services.auth_service import login_user

register_bp = Blueprint("register_bp", __name__)
login_bp = Blueprint("login_bp", __name__)

@register_bp.route("/", methods=["POST"])
def regsiter_route():

    #get request from user
    data = request.json
    #define the fields for the form when user wants to register
    required_data = ["username", "email", "password"]

    #checking the data must be required when user wants to input their fields
    if not all(fields in data and data[fields] for fields in required_data):
        return jsonify({
            "data": None,
            "message": "Failed to validate the fields of the user",
            "success": False,
        }), 403

    #put the request to reg_user function
    users, msg = register_user(
        input_username=data["username"],
        input_email=data["email"],
        input_password=data["password"]
    )

    #if not user , then return a error 422 or http badrequest
    if not users :
        return jsonify({
            "data": None,
            "message": msg,
            "success": False
        }), 403

    #define the response structure from request client
    users_data = {
        "username": users.username,
        "email": users.email,
    }

    #return the result of the routers
    return jsonify({
        "message": "Register has been successfully!",
        "data": users_data,
        "success": True
    }), 201

@login_bp.route("/", methods=["POST"])
def login_route():

    #get request as a json request
    data = request.json

    #checking and validate for a required fields in user request!
    required = ["username", "password"]
    if not all(fields in data and data[fields] for fields in required):
        return jsonify({
            "message": "The field must be required!",
            "data": None,
            "success": False,
        }), 403
    
    #mapping into a form request in a login_user 
    user_login, token, msg = login_user(
        input_username=data["username"],
        input_password=data["password"]
    )

    #validate the users login must be exist when user wants to login himself
    if not user_login:
        return jsonify({
            "message": msg,
            "data": None,
            "success": False
        }), 403

    #mapping the data again before we 
    users_login_data = {
        "username": user_login.username,
        "email": user_login.email,
        "profile_image": user_login.profile_image,
        "thumbnail_img": user_login.thumbnail_img,
        "token": token
    }

    return jsonify({
        "message": "Successfully to login as a user!",
        "data": users_login_data,
        "success": True,
    }), 200

