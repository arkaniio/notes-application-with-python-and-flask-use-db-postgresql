from app.services.note_service import create_note, get_public_note, get_public_notes_by_user_id, get_not_by_slug, update_notes
from app.services.note_service import delete_notes
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from app.utils.json import response_error
from app.utils.json import response_success
from flask import Blueprint, request

note_bp = Blueprint("create_note_bp", __name__)

@note_bp.route("/", methods=["POST"])
@jwt_required()
def create_note_routes():

    #define the user id from jwt extended
    user_id = get_jwt_identity()

    #define the request of the client
    data = request.get_json()

    #validate if the data is not exist
    if not data:
        return response_error(None)

    password = data.get("password") or None
    password_hint = data.get("password_hint") or None
    slug = data.get("slug")

    #looping into a function that contain the create note function
    notes, msg = create_note(
        user_id=user_id, 
        title=data["title"], 
        content=data["content"],
        slug=slug,
        status=data["status"],
        password=password,
        password_hint=password_hint)

    #checking if the notes is not exist
    if not notes:
        return response_error(msg)
    
    return response_success(notes)

@note_bp.route("/", methods=["GET"])
def get_public_note_routes():

    #request data for json use args because we want to use the query on url parameters
    q = request.args.get("q", type=str)
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    order = request.args.get("order", default="desc", type=str)
    sort = request.args.get("sort", default="created_at", type=str)

    #put that on the params of this function
    notes, meta, msg = get_public_note(
        q=q,
        page=page,
        per_page=per_page,
        sort=sort,
        order=order,
    )

    #validate if the notes and meta is not exist
    if not notes and not meta:
        return response_error(msg)
    
    return response_success(notes, meta)

@note_bp.route("/", methods=["GET"])
@jwt_required()
def get_notes_by_user_id():

    #user id 
    user_id = get_jwt_identity()

    #request data for json use args because we want to use the query on url parameters
    q = request.args.get("q", type=str)
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    order = request.args.get("order", default="desc", type=str)
    sort = request.args.get("sort", default="created_at", type=str)

    #put that on the params of this function
    notes, meta, msg = get_public_notes_by_user_id(
        user_id=user_id,
        q=q,
        page=page,
        per_page=per_page,
        sort=sort,
        order=order,
    )

    #validate if the notes and meta is not exist
    if not notes and not meta:
        return response_error(msg)
    
    return response_success(notes, meta)

@note_bp.route("/<string:slug>", methods=["GET"])
@jwt_required(optional=True)
def get_notes_by_slug(slug):

    #define the password in url params
    password = request.args.get("password", type=str)

    #define the user id from token
    user_id = get_jwt_identity()

    #if the password none and password has been requested in json type
    if password is None and request.is_json:
        body = request.get_json()
        password = body.get("password")
    
    #looping the data to put their in the function
    notes, msg, hint = get_not_by_slug(
        user_id=user_id,
        slug=slug,
        password=password
        )
    
    #validate if the note is not exist
    if not notes:
        if msg in ("Password has been required", "Invalid password"):
            return response_error(msg, hint)
        return response_error(msg)

    return response_success(notes)

@note_bp.route("/<string:note_id>", methods=["PUT"])
@jwt_required()
def update_note_routes(note_id):

    #get the user id from token 
    user_id = get_jwt_identity()

    #request from a user when user wants to update their data
    data = request.get_json()

    #looping into a function update
    notes, msg = update_notes(user_id=user_id, note_id=note_id, data=data)

    #validate if the update is failed or invalid
    if not notes:
        return response_error(msg)

    return response_success(notes)

@note_bp.route("/<string:note_id>", methods=["DELETE"])
@jwt_required()
def delete_notes_routes(note_id):

    #get user id identity
    user_id = get_jwt_identity()

    #looping into a function delete in service
    notes_delete, msg = delete_notes(note_id=note_id, user_id=user_id)

    #validate if the delete is invalid or is not exist
    if not notes_delete:
        return response_error(msg)
    
    return response_success(notes_delete)
