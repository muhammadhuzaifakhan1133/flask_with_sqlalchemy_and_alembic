from models.models.complaint_model import Complaint
from models.models.complaint_status_model import ComplaintStatus
from models.models.complaint_type_model import ComplaintType
from models.setup import db
from models.models.user_model import User
from sqlalchemy import select, func
from datetime import datetime, timedelta

from services.row_to_dict_service import as_dict

def superadmin_dashboard_controller():
    staff_count = db.session.execute(select(func.count("*").label("staff_count")).where(User.role_type=="staff").select_from(User)).one()._asdict()
    admin_count = db.session.execute(select(func.count("*").label("admin_count")).where(User.role_type=="admin").select_from(User)).one()._asdict()
    now =  datetime.utcnow()
    total_seven_day_complaint_count = db.session.query(func.count().label('total_seven_day_count')).filter(Complaint.created_at >= now - timedelta(days=7)).first()._asdict()
    total_thirty_day_complaint_count = db.session.query(func.count().label('total_thirty_day_count')).filter(Complaint.created_at >= now - timedelta(days=30)).first()._asdict()
    resolved_status_id = db.session.query(ComplaintStatus.id).filter(ComplaintStatus.name == "RESOLVED").scalar()
    resolved_seven_day_complaint_count = db.session.query(func.count().label('resolved_seven_day_count')).filter(Complaint.created_at >=  now - timedelta(days=7)).filter(Complaint.complaint_status_id == resolved_status_id).first()._asdict()
    resolved_thirty_day_complaint_count = db.session.query(func.count().label('resolved_thirty_day_count')).filter(Complaint.created_at >=  now - timedelta(days=30)).filter(Complaint.complaint_status_id == resolved_status_id).first()._asdict()
    top_five_statuses_result = db.session.execute(select(Complaint.complaint_type_id.label("complaint_type_id"), (select(ComplaintType.name).where(ComplaintType.id == Complaint.complaint_type_id).scalar_subquery().correlate(Complaint)).label("name"), func.count("*").label("count")).select_from(Complaint).group_by(Complaint.complaint_type_id).order_by(func.count("*").desc()).limit(5)).all()
    top_five_statuses = []
    for status in top_five_statuses_result:
        top_five_statuses.append(status._asdict())
    
    return {
        "users": staff_count | admin_count,
        "complaints": total_seven_day_complaint_count | total_thirty_day_complaint_count | resolved_seven_day_complaint_count | resolved_thirty_day_complaint_count,
        "top_five_statuses": top_five_statuses
    }
