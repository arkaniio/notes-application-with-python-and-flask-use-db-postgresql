from app.models.user import User
from app.models.user import db
import os, uuid
from werkzeug.utils import secure_filename

def is_Valid(filename):

    #list of the type for filename
    file = {"jpeg", "png", "jpg"}

    #convert into a path file from os
    ext = os.path.splitext(filename.lower())[1].replace(".", "")
    return ext in file

def random_name(filename):

    #make the new name of filename
    file = os.path.splitext(filename)[1]

    #convert it into string type
    name = f"{uuid.uuid4()}{file}"
    return name

def get_user_byId(user_id):

    try:
        #get the user identity
        user = User.query.get(user_id)

        #validate the user if not exists
        if not user:
            return None, "The user has not exist in db that you want !"
    
        return user.to_Json(), "User has been detected and get successfully!"
    
    except Exception as e:
        return None, f"Failed to get the user ! {e}"
    
def update_user(user_id, data, profile_image=None, thumbnail_img=None):

    #get the user identity
    user = User.query.get(user_id)

        #validate the user if user not exist
    if not user:
        return None, "The user has not exist in db that you want!"
    
    try:

        #validate if the user wants to update their password
        if "password" in data and data["password"]:
            user.set_password(data["password"])
        
        #loop the data if user wants to update their username and email
        for field in ["username", "email"]:
            if field in data and data[field]:
                setattr(user, field, data[field])
        
        #make the folder to save the image from there
        os.makedirs("uploads", exist_ok=True)
        
        #if the type of file profile image is mathing with the function that cehcking the type of file
        if profile_image and is_Valid(profile_image.filename):
            name = random_name(filename=profile_image.filename)
            filename_profile = secure_filename(name)
            path = os.path.join("uploads", filename_profile)
            profile_image.save(path)
            if user.profile_image:
                file_name_old_profileImage = user.profile_image.replace("/uploads/", "")
                path_name_old_profileImage = os.path.join("uploads", file_name_old_profileImage)
                if os.path.exists(path=path_name_old_profileImage):
                    os.remove(path=path_name_old_profileImage)
            setattr(user, "profile_image", f"/uploads/{filename_profile}")
        
        #if the type of file thumbnail_img is mathing with the function tgat checking the type of file
        if thumbnail_img and is_Valid(thumbnail_img.filename):
            name = random_name(filename=thumbnail_img.filename)
            filename_thumbnail = secure_filename(name)
            path = os.path.join("uploads", filename_thumbnail)
            thumbnail_img.save(path)
            if user.thumbnail_img:
                file_name_old_thumbnailImg = user.thumbnail_img.replace("/uploads/", "")
                path_name_old_thumbnailImg = os.path.join("uploads", file_name_old_thumbnailImg)
                if os.path.exists(path=path_name_old_thumbnailImg):
                    os.remove(path=path_name_old_thumbnailImg)
            setattr(user, "thumbnail_img", f"/uploads/{filename_thumbnail}")
        
        #commit if the update has been successfully
        db.session.add(user)
        db.session.commit()
        return user.to_Json(), f"Update the {user.username} has been successfully!"
    
    except Exception as e:
        db.session.rollback()
        return None, f"Failed to update the user! {e}"
