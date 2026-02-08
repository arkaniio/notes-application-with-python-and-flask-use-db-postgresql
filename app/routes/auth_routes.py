from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user

register_bp = Blueprint("register_bp", __name__)

@register_bp.route("/", methods=["POST"])

def regsiter_route():

    #get request from user
    data = request.json
    #define the fields for the form when user wants to register
    required_data = ["username", "email", "password"]

    #checking the data must be required when user wants to input their fields
    if not all(fields in request and data[required_data] for fields in required_data):
        return jsonify({
            "data": None,
            "message": "Failed to validate the fields of the user",
            "success": False,
        }), 403

    #put the request to reg_user function
    users, msg = register_user(
        input_username=data["username"],
        input_email=data["email"],
        input_password=["password"]
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
        "email": users.email
    }

    #return the result of the routers
    return jsonify({
        "data": users_data,
        "message": "Register has been successfully!",
        "success": True
    }), 201
