from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.response_services import display_response
from controllers.dashboards import superadmin_dashboard as SuperAdminDashboard


superadmin_dashboard_bp = Blueprint("superadmin-dashboard-type", "dashboard_services")
allowed_roles = ["superadmin"]

@superadmin_dashboard_bp.route("/dashboard/superadmin", methods=["GET"])
@jwt_required()
def superadmin_dashboard_route():
    user_data = get_jwt_identity()
    if (user_data.get("role") not in allowed_roles):
        return display_response(status_code=400, errors=["Unauthenticated user"])
    counts = SuperAdminDashboard.superadmin_dashboard_controller()
    return display_response(message="superadmin dashboard", data=counts)