from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.response_services import display_response
from controllers.complaints import update_complaint as UpdateComplaint

update_complaint_bp = Blueprint("update-complaint", "user_service")
allowed_roles = ['superadmin', 'admin']

@update_complaint_bp.route('/complaint/update/<comp_id>', methods=["PUT"])
@jwt_required()
def update_complaint_route(comp_id):
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
    isUpdated = UpdateComplaint.update_complaint_controller(
        id=comp_id,
        title=data.get("title"),
        description=data.get("description"),
        complaint_type_id=data.get("complaint_type_id"),
    )
    if (isUpdated):
        return display_response(message="Complaint updated successfully")
    else:
        return display_response(status_code=400, errors=["No update detect in given data or Invalid complaint id"])
    
def validate_data(data):
    is_field_given = False
    if (data.get("title") is not None) and (len(data.get("title").strip()) > 0):
        is_field_given = True
    if (data.get("description") is not None) and (len(data.get("description").strip()) > 0):
        is_field_given = True
    if (data.get("complaint_type_id") is not None) and (len(str(data.get("complaint_type_id")).strip()) > 0):
        is_field_given = True
    if not is_field_given:
        return ["atleast one field is required (title, description, complaint_type_id)"]
    return []