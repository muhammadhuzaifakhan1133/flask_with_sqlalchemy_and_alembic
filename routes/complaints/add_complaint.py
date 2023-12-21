from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.response_services import display_response
from controllers.complaints import add_complaint as AddComplaint

add_complaint_bp = Blueprint("add-complaint", "user_service")
allowed_roles = ['superadmin', 'admin']

@add_complaint_bp.route('/complaint/add', methods=["POST"])
@jwt_required()
def add_complaint_route():
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
    complaint_id = AddComplaint.add_complaint_controller(
        title=data.get("title"),
        description=data.get("description"),
        complaint_type_id=data.get("complaint_type_id"),
    )
    return display_response(message="Complaint added successfully", data={
        "id": complaint_id,
    })
    
def validate_data(data):
    error_msgs = []
    if (data.get("title") is None) or (len(data.get("title").strip()) == 0):
        error_msgs.append("title is required")
    if (data.get("description") is None) or (len(data.get("description").strip()) == 0):
        error_msgs.append("description is required") 
    if (data.get("complaint_type_id") is None) or (len(str(data.get("complaint_type_id")).strip()) == 0):
        error_msgs.append("complaint_type_id is required")
    return error_msgs