from flask import jsonify

# make the response for a success response 
def response_success(data, message="success", status_code=200, success=True, meta=None):

    response = {
        "data": data,
        "message": message,
        "success": success,
    }

    if meta is not None:
        response["meta"] = meta

    return jsonify(response), status_code

# make the response for a error response
def response_error(data, message="failed", status_code=400, success=False, hint=None):

    response = {
        "data": data,
        "message": message,
        "success": success
    }

    if hint is not None:
        response["hint"] = hint
    
    return jsonify(response)