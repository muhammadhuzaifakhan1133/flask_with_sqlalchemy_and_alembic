from sqlalchemy import select, update
from models.models.complaint_status_model import ComplaintStatus
from models.models.complaint_model import Complaint
from models.setup import db

def complete_complaint_controller(complaint_id):
    status_query = select(ComplaintStatus.id).where(ComplaintStatus.name=="RESOLVED")
    status_id = db.session.execute(status_query).scalar()
    query = update(Complaint).where(
        Complaint.id==complaint_id
    ).values(
        complaint_status_id=status_id
    )
    result = db.session.execute(query)
    db.session.commit()
    return result.rowcount > 0