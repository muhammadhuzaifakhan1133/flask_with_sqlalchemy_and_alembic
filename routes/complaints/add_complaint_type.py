from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.complaints import add_complaint_type as AddComplaintType
from services.response_services import display_response


add_complaint_type_bp = Blueprint("add-complaint-type", "complaint_services")
allowed_roles = ["superadmin", "admin"]

@add_complaint_type_bp.route("/complaint/add_type", methods=["POST"])
@jwt_required()
def add_complaint_type_route():
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
    type_id = AddComplaintType.add_complaint_type_controller(name=data.get("name"))
    return display_response(message="Complaint type added successfully", data={
        "id": type_id,
    })

    
def validate_data(data):
    error_msgs = []
    if (data.get("name") is None) or (len(data.get("name").strip()) == 0):
        error_msgs.append("name is required")
    return error_msgs