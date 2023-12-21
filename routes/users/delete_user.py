from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.response_services import display_response
from controllers.users import delete_user as DeleteUser

delete_user_bp = Blueprint("delete-user", "user_service")
allowed_roles = ['superadmin']

@delete_user_bp.route('/user/delete/<uid>', methods=["DELETE"])
@jwt_required()
def delete_user_route(uid):
    user_data = get_jwt_identity()
    if (user_data.get("role") not in allowed_roles):
        return display_response(status_code=400, errors=["Unauthenticated user"])
    isDeleted = DeleteUser.delete_user_controller(
        id=uid
    )
    if (isDeleted):
        return display_response(message="User deleted successfully")
    else:
        return display_response(status_code=400, errors=["Invalid user id"])
