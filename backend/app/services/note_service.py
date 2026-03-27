from app import db
from app.models.notes import Note
from app.models.user import User
import uuid
from datetime import datetime
from sqlalchemy import asc, desc

def create_note(user_id, title, content, slug, status="public", password=None, password_hint=None):

    #get the user
    user = User.query.get(user_id)

    #checking if the user not exist
    if not user:
        return None, "User is not exist!"
    
    #checking the type of the note status
    if status not in {"private", "public", "protected"}:
        return None, "The type of the status is not exist!"

    #make the slug
    slug = str(uuid.uuid4())

    #looping into a Note class db
    note = Note(
        user_id=user_id,
        title=title,
        content=content,
        status=status,
        slug=slug,
        password_hint=(password_hint or None)
    )

    #check if the status is protected , the password must be required
    if status == "protected" and not password:
        return None, "Status protected must have a password!"
    
    #check if the status is protected and the password is exist, it would be a hashing the password
    if status == "protected" and password:
        note.set_password(password)
    
    #commit into a db
    try:

        db.session.add(note)
        db.session.commit()
        
        return note.to_Json(include_user=True), "Create a new note has been successfully!"
    
    except Exception as e:

        db.session.rollback()
        return None, f"Create a new note was not successfully {e}"

def get_public_note(q=None, page=1, per_page=10, sort="created_at", order="desc"):

    #base query
    notes = Note.query.filter(Note.deleted_at == None, Note.status == "public")

    #validate if the status note is not a public status
    if not notes:
        return None, "Invalid note status!"
    
    #if the q is exist \ the query search on the params of postman url
    if q:
        notes = notes.filter(Note.title.ilike(f"%{q}%") | Note.content.ilike(f"%{q}%"))
    
    #make the mapping of the sort
    sort_map = {
        "title": Note.title,
        "created_at": Note.created_at,
        "updated_at": Note.updated_at,
        "username": User.username,
    }

    #sort the data
    sort_mapping_notes = sort_map.get(sort, Note.created_at)

    if order == "asc":
        notes = notes.order_by(asc(sort_mapping_notes))
    else:
        notes = notes.order_by(desc(sort_mapping_notes))
    
    #make the pagination of the notes data
    paginate = notes.paginate(page=page, per_page=per_page, error_out=False)

    #looping into a new variable
    data_notes_paginate = [note.to_Json(include_user=True) for note in paginate.items]

    #validate if the data notes is not exist
    if not data_notes_paginate:
        return None, "Failed to do paginate with notes data"
    
    #make the response of the final api
    meta_data = {
        "page": paginate.page,
        "per_page": paginate.per_page,
        "total": paginate.total,
        "pages": paginate.pages,
        "sort": sort,
        "order": order,
        "q": q or ""
    }

    return data_notes_paginate, meta_data, "Get the public note has been successfully!"

def get_public_notes_by_user_id(user_id, page=1, per_page=10, q=None, order="desc", sort="created_at"):

    #base query
    notes = Note.query.filter(Note.deleted_at == None, Note.status == "public", Note.user_id == user_id)

    #validate the user id if the user id is not exist
    if not user_id:
        return None, "Invalid user id!"

    #validate if the status note is not a public status
    if not notes:
        return None, "Invalid note status!"
    
    #if the q is exist \ the query search on the params of postman url
    if q:
        notes = notes.filter(Note.title.ilike(f"%{q}%") | Note.content.ilike(f"%{q}%"))
    
    #make the mapping of the sort
    sort_map = {
        "title": Note.title,
        "created_at": Note.created_at,
        "updated_at": Note.updated_at,
    }

    #sort the data
    sort_mapping_notes = sort_map.get(sort, Note.created_at)

    if order == "asc":
        notes = notes.order_by(asc(sort_mapping_notes))
    else:
        notes = notes.order_by(desc(sort_mapping_notes))
    
    #make the pagination of the notes data
    paginate = notes.paginate(page=page, per_page=per_page, error_out=False)

    #looping into a new variable
    data_notes_paginate = [note.to_Json(include_user=True) for note in paginate.items]

    #validate if the data notes is not exist
    if not data_notes_paginate:
        return None, "Failed to do paginate with notes data"
    
    #make the response of the final api
    meta_data = {
        "page": paginate.page,
        "per_page": paginate.per_page,
        "total": paginate.total,
        "pages": paginate.pages,
        "sort": sort,
        "order": order,
        "q": q or ""
    }

    return data_notes_paginate, meta_data, "Get the public note has been successfully!"

def get_not_by_slug(user_id, slug, password):

    #get note
    note = Note.query.filter(slug == slug).first()

    #validate if the note is not exist
    if not note:
        return None, "Note not found!", None
    
    #if the status of the note is public
    if note.status == "public":
        return note.to_Json(include_user=False), "Get note has been successfully!", None
    
    #if the status is private
    if note.status == "private":
        if user_id != note.user_id:
            return None, "Can't see the private note someone!", None
        return note.to_Json(include_user=False), "Get note has been successfully!", None
    
    #if the status of not is protected
    if note.status == "protected":

        #check if the password has not exist in the request
        if not password:
            return None, "Password has been required", note.password_hint

        #checking if the password matching with the password hint on the db
        if not note.check_password(password):
            return None, "Invalid password", note.password_hint
        
        return note.to_Json(include_user=False), "Get note has been successfully", None
    
    return None, "Note status is invalid", None

def update_notes(note_id, data, user_id):

    #base query for find the right user
    note = Note.query.filter(Note.id == note_id, Note.deleted_at == None).first()

    #validate if the note is not exist
    if not note:
        return None, "Note is not exist or is not found!"

    #parsing and conditioning the data
    try: 

        #if the user wants to update their title
        if "title" in data:
            note.title = data["title"]
        
        #if the user wants to update their content
        if "content" in data:
            note.content = data["content"]
        
        #if the user wants to update their status
        if "status" in data:
            note.status = data["status"]
            
            status = data["status"]

            #checking if the status type is invalid or not
            if status not in ["private", "public", "protected"]:
                return None, "Invalid status type!"
            
            note.status = status

            #if the status is protected
            if status == "protected":
                #looping because the status is enum in database
                password = data.get("password")
                password_hint = data.get("password_hint")

                if not password or not password_hint:
                    return None, "Password must be required!"

                note.set_password(password)
                note.password_hint = password_hint
        else:
            password = None
            password_hint = None
        
        db.session.commit()
        return note.to_Json(include_user=True), "Update the notes data has been successfully!"

    except Exception as e:
        db.session.rollback()
        return None, f"Failed to update the notes {e}"

def delete_notes(note_id, user_id):

    #base query to get the note id from database
    note = Note.query.filter_by(id = note_id).first()

    #update the deleted at in db
    note.deleted_at = datetime.now().isoformat()

    #checking if the note is not exist
    if not note:
        return None, "The note is not founc or not exist!"
    
    #checking if the others user note cant delete the others user note
    if note.user_id != user_id:
        return None, "Failed to delete others note!"
    
    db.session.delete(note)
    db.session.commit()
    return True, "Delete user has been successfully!"
