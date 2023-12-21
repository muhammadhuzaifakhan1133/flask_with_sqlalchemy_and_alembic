from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.response_services import display_response
from controllers.complaints import view_staff_complaints as ViewStaffComplaints

view_staff_complaints_bp = Blueprint("view-staff-complaints", "complaint_services")
allowed_roles =["staff"]

@view_staff_complaints_bp.route("/complaint/view")
@jwt_required()
def view_staff_complaints_route():
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
    complaints = ViewStaffComplaints.view_staff_complaints_controller(
        status_id=data.get("status_id"),
        user_id=user_data.get("id")
    )
    print(complaints)
    return display_response(data=complaints)
    
def validate_data(data):
    error_msgs = []
    if (data.get("status_id") is None) or (len(str(data.get("status_id")).strip()) == 0):
        error_msgs.append("status_id is required")
    return error_msgs

