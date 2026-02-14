from app.services.user_service import get_user_byId
from app.services.user_service import update_user
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask import Blueprint
from app.utils.json import response_error
from app.utils.json import response_success
from flask import request

getIdUser_bp = Blueprint("get_user_bp", __name__)
updateIdUser_bp = Blueprint("update_user_bp", __name__)

# for checking the token jwt before user start to access this method
@getIdUser_bp.route("/", methods=["GET"])
@jwt_required()

def get_by_id_routes():

    #get the id from token user
    token_id_user = get_jwt_identity()

    #put the token into a service user
    users_profile, msg = get_user_byId(user_id=token_id_user)

    #make the validate for checking users exist
    if not users_profile:
        return response_error(msg)
    
    #validate again
    if not users_profile:
        return response_error(msg)

    return response_success(users_profile)

#checking the jwt is required again
@updateIdUser_bp.route("/", methods=["PUT"])
@jwt_required()

def update_user_routes():

    #get user id identity
    user_id = get_jwt_identity()

    #validate the request
    data_request = request.form.to_dict()

    #file form for profile image and thumbnail image and to get the data from request
    profile_img = request.files.get("profile_image")
    thumbnail_image = request.files.get("thumbnail_img")

    #validate if the user not send the data , profile_image and the thumbnail image
    if not data_request and not profile_img and not thumbnail_image:
        return response_error(None)
    
    #final return to loop the user data
    users, msg = update_user(user_id=user_id, data=data_request, profile_image=profile_img, thumbnail_img=thumbnail_image)

    #validate again if the users is not exist
    if not users:
        return response_error(msg)
    
    #final return
    return response_success(users)
