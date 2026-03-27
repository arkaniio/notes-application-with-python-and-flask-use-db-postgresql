from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.json import response_error, response_success
from app.services.like_service import toggle_like, get_like_by_user_id

like_bp = Blueprint("like_bp_route", __name__)
@like_bp.route("/<string:note_id>", methods=["POST"])
@jwt_required()
def like_route(note_id):

    #define the user_id form token identity
    user_id = get_jwt_identity()

    like, msg = toggle_like(note_id=note_id, user_id=user_id)

    #validate if the like is not exist
    if not like:
        return response_error(msg)
    
    return response_success(like)
@like_bp.route("/", methods=["GET"])
@like_bp.route("/<string:note_id>", methods=["GET"])
@jwt_required()
def get_all_like(note_id=None):
    user_id = get_jwt_identity()
    likes, msg = get_like_by_user_id(user_id=user_id, note_id=note_id)
    
    # Return empty list if no likes found instead of error
    if likes is None:
        return response_error(msg)
    
    return response_success(likes)
