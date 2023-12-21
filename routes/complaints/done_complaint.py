import os
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import services.file_services as FileServices
from services.response_services import display_response
from datetime import datetime
from controllers.complaints import done_complaint as DoneComplaint

done_complaint_bp = Blueprint("done-complaint", "complaint_services")
allowed_roles =["superadmin", "admin", "staff"]

@done_complaint_bp.route("/complaint/<comp_id>/done", methods=["PATCH"])
@jwt_required()
def done_complaint_route(comp_id):
    user_data = get_jwt_identity()
    if (user_data.get("role") not in allowed_roles):
        return display_response(status_code=400, errors=["Unauthenticated user"])
    if 'file' not in request.files:
        return display_response(status_code=400, errors=["file is required"])
    file = request.files['file']
    if not FileServices.allowed_file(file.filename):
        return display_response(status_code=400, errors=["file type is not allowed"])
    file_extension = FileServices.get_extension(file.filename)
    new_filename = str(int(datetime.now().timestamp()))+'.'+file_extension
    file.save(os.path.join(FileServices.UPLOAD_FOLDER, new_filename))
    isUpdated = DoneComplaint.done_complaint_controller(
        complaint_id=comp_id,
        filename=new_filename
    )
    if (isUpdated):
        return display_response(message="Complaint doneed successfully")
    else:
        return display_response(status_code=400, errors=["Invalid complaint_id or complaint already marked done"])