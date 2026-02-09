from app.services.user_service import get_user_byId
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask import Blueprint
from app.utils.json import response_error
from app.utils.json import response_success
from app.models.user import to_Json

getIdUser_bp = Blueprint("get_user_bp", __name__)

# for checking the token jwt before user start to access this method
@jwt_required()
@getIdUser_bp.route("/", get_user_byId)

def get_by_id_routes():

    #get the id from token user
    token_id_user = get_jwt_identity()

    #put the token into a service user
    users_profile, msg = get_user_byId(user_id=token_id_user)

    #make the validate for checking users exist
    if not users_profile:
        return response_error(msg)
    
    #looping into a json response
    users_data = to_Json(
        users_profile.username, 
        users_profile.email,
        users_profile.profile_image,
        users_profile.thumbnail_img,
        users_profile.created_at
        )
    
    #validate again
    if not users_data:
        return response_error(msg)

    return response_success(users_data)