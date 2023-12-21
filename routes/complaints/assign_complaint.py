from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.response_services import display_response
from controllers.complaints import assign_complaint as AssignComplaint

assign_complaint_bp = Blueprint("assign-complaint", "complaint_services")
allowed_roles =["superadmin", "admin"]

@assign_complaint_bp.route("/complaint/<comp_id>/assign", methods=["PATCH"])
@jwt_required()
def assign_complaint_route(comp_id):
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
    isUpdated = AssignComplaint.assign_complaint_controller(
        complaint_id=comp_id,
        user_id=data.get("staff_id")
    )
    if (isUpdated):
        return display_response(message="Complaint assigned successfully")
    else:
        return display_response(status_code=400, errors=["No update detect in given staff_id or Invalid complaint id or Invalid staff id"])

def validate_data(data):
    error_msgs = []
    if (data.get("staff_id") is None) or (len(str(data.get("staff_id")).strip()) == 0):
        error_msgs.append("staff_id is required")
    return error_msgs