from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.response_services import display_response
from controllers.users import update_user as UpdateUser

update_user_bp = Blueprint("update-user", "user_service")
allowed_roles = ['superadmin']

@update_user_bp.route('/user/update/<uid>', methods=["PUT"])
@jwt_required()
def update_user_route(uid):
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
    isUpdated = UpdateUser.update_user_controller(
        id=uid,
        email=data.get("email"),
        phone=data.get("phone"),
        password=data.get("password"),
        role_type=data.get("role_type"),
    )
    if (isUpdated):
        return display_response(message="User updated successfully")
    else:
        return display_response(status_code=400, errors=["No update detect in given data or Invalid user id"])
    
def validate_data(data):
    is_field_given = False
    if (data.get("email") is not None) and (len(data.get("email").strip()) > 0):
        is_field_given = True
    if (data.get("phone") is not None) and (len(data.get("phone").strip()) > 0):
        is_field_given = True
    if (data.get("password") is not None) and (len(data.get("password").strip()) > 0):
        is_field_given = True
    if (data.get("role_type") is not None) and (len(data.get("role_type").strip()) > 0):
        is_field_given = True
    if not is_field_given:
        return ["atleast one field is required (email, phone, password, role_type)"]
    return []