from flask import Blueprint, send_from_directory, current_app, abort
from werkzeug.utils import secure_filename
import os

file_routes_bp = Blueprint("file_route_bp", __name__)

@file_routes_bp.route("/<path:filename>", methods=["GET"])
def find_file(filename):

    #sanitasi nama file
    save_file = secure_filename(filename)

    #cari folder file
    path_folder = current_app.config.get("UPLOAD_FOLDER", os.path.join(os.getcwd(), "uploads"))

    #cari file
    path_final = os.path.join(save_file, path_folder)

    if not os.path.exists(path_final):
        abort(400, description="Failed to see the file to client")
    
    return send_from_directory(path_final, save_file)