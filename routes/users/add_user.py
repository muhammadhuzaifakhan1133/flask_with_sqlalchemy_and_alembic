from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.response_services import display_response
from controllers.users import add_user as AddUser

add_user_bp = Blueprint("add-user", "user_service")
allowed_roles = ['superadmin']

@add_user_bp.route('/user/add', methods=["POST"])
@jwt_required()
def add_user_route():
    user_data = get_jwt_identity()
    if (user_data.get("role") not in allowed_roles):
        return display_response(status_code=400, errors=["Unauthenticated user"])
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
    user_id = AddUser.add_user_controller(
        email=data.get("email"),
        phone=data.get("phone"),
        password=data.get("password"),
        role_type=data.get("role_type"),
    )
    return display_response(message="User added successfully", data={
        "id": user_id,
    })
    
def validate_data(data):
    error_msgs = []
    if (data.get("email") is None) or (len(data.get("email").strip()) == 0):
        if (data.get("phone") is None) or (len(data.get("phone").strip()) == 0):
            error_msgs.append("email or phone is required")
    if (data.get("password") is None) or (len(data.get("password").strip()) == 0):
        error_msgs.append("password is required") 
    if (data.get("role_type") is None) or (len(data.get("role_type").strip()) == 0):
        error_msgs.append("role_type is required")
    return error_msgs