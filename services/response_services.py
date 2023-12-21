def display_response(status_code=200, errors=[], message="", data=[]):
    return ({
        "status_code": status_code,
        "message": message,
        "errors": errors,
        "data": data,
    }, status_code)