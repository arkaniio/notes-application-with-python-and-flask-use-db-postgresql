from flask import jsonify

# make the response for a success response 
def response_success(data, message="success", status_code=200, success=True):
    return jsonify({
        "message": message,
        "data": data,
        "success": success,
    }), status_code

# make the response for a error response
def response_error(data, message="failed", status_code=400, success=False):
    return jsonify({
        "message": message,
        "data": data,
        "success": success
    }), status_code