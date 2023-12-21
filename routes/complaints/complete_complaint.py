from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.response_services import display_response
from controllers.complaints import complete_complaint as CompleteComplaint

complete_complaint_bp = Blueprint("complete-complaint", "complaint_services")
allowed_roles =["superadmin", "admin"]

@complete_complaint_bp.route("/complaint/<comp_id>/complete", methods=["PATCH"])
@jwt_required()
def complete_complaint_route(comp_id):
    user_data = get_jwt_identity()
    if (user_data.get("role") not in allowed_roles):
        return display_response(status_code=400, errors=["Unauthenticated user"])
    isUpdated = CompleteComplaint.complete_complaint_controller(
        complaint_id=comp_id,
    )
    if (isUpdated):
        return display_response(message="Complaint completeed successfully")
    else:
        return display_response(status_code=400, errors=["Invalid complaint_id or complaint already marked complete"])