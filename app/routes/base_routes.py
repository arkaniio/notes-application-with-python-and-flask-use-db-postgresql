from flask import Blueprint, jsonify

base = Blueprint("base_bp", __name__)

@base.route("/", methods=['GET'])

def home ():
    return jsonify({"message": "The api is Running!"})

