from models.setup import db
from models.models.complaint_model import Complaint
from models.models.complaint_status_model import ComplaintStatus
from sqlalchemy import select

def add_complaint_controller(title, description, complaint_type_id):
    query = select(ComplaintStatus.id).where(ComplaintStatus.name=="PENDING")
    status_id = db.session.execute(query).scalar()
    print(status_id)
    complaint = Complaint(
        title=title, 
        description=description, 
        complaint_type_id=complaint_type_id, 
        complaint_status_id=status_id
    )
    db.session.add(complaint)
    db.session.commit()
    return complaint.id