from app import db
from app.models.notes import Note
from app.models.likes import Like
from app.models.user import User

def toggle_like(note_id, user_id):

    #base query for find the user
    user = User.query.get(user_id)

    #validate if the user is not exist
    if not user:
        return None, "Failed to find the id!"
    
    #base query for find the note id
    note = Note.query.get(note_id)

    #validate if the note is not exist in the db
    if not note:
        return None, "Failed to find the not id!"
    
    #base query for make sure that note id and user id is mathcing with the like note id and like user id
    like = Like.query.filter((Like.note_id == note.id) & (Like.user_id == user.id)).first()
    
    if like:
        try:
            #delete the like if the user has been touched it
            db.session.delete(like)
            db.session.commit()
            return True, "Unlike has been successfully"
        except Exception as e:
            db.session.rollback()
            return None, f"Unlike was not successed! {e}"
    else:
        try:
            #add the like in db
            likes_data = Like(user_id=user_id, note_id=note_id)

            #validate if the likes data is not exist
            if not likes_data:
                return None, "Failed to add the like to db!"
            
            db.session.add(likes_data)
            db.session.commit()
            return likes_data.to_Json(include_user=True, include_note=True), "Add the like has been successfully!"
        except Exception as e:
            db.session.rollback()
            return None, "Add like was not successed!"

def get_like_by_user_id(user_id, note_id):
    
    #base query for find the user
    user = User.query.get(user_id)

    #validate if the user is not exist
    if not user:
        return None, "Failed to find the id!"
    
    #base query for find the like by user id
    likes = Like.query.filter((Like.note_id == note_id) & (Like.user_id == user.id)).all()
    
    if not likes:
        return None, "Failed to find the like!"
    
    return [like.to_Json(include_user=True, include_note=True) for like in likes], "Get like has been successfully!"
