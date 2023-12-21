from controllers.users import login_user as LoginUser
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from services.response_services import display_response


login_user_bp = Blueprint("login-user", "user_service")

@login_user_bp.route("/user/login", methods=["POST"])
def login_user_route():
    if not request.is_json:
        return display_response(
            errors=[
                "API accepts JSON data"
            ],
            status_code=400
        )
    data = request.get_json()
    if len((errors := validate_data(data))) > 0:
        return display_response(errors=errors, status_code=400)
    userId, role = LoginUser.login_user_controller(
        email=data.get("email"),
        phone=data.get("phone"),
        password=data.get("password"),
    )
    if (userId != None):
        token = create_access_token(identity={
                "id": userId,
                "role": role,
            })
        return display_response(
            message="user login successfully",
            data={
                "id": userId, 
                "token": token,
            }
        )
    else:
        return display_response(
            errors=["Invalid email or password"],
            status_code=400,
        )


def validate_data(data):
    error_msgs = []
    if (data.get("email") is None) or (len(data.get("email").strip()) == 0):
        if (data.get("phone") is None) or (len(data.get("phone").strip()) == 0):
            error_msgs.append("email or phone is required")
    if (data.get("email") is not None) and (data.get("phone") is not None):
        error_msgs.append("input either email or phone, not both")
    if (data.get("password") is None) or (len(data.get("password").strip()) == 0):
        error_msgs.append("password is required")
    return error_msgs