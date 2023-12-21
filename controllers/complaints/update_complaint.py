from sqlalchemy import update
from models.setup import db
from models.models.complaint_model import Complaint

def update_complaint_controller(id, title, description, complaint_type_id):
    query = update(Complaint).where(Complaint.id == id)
    if title:
        query = query.values(title=title)
    if description:
        query = query.values(description=description)
    if complaint_type_id:
        query = query.values(complaint_type_id=complaint_type_id)
    result = db.session.execute(query)
    db.session.commit()
    return result.rowcount > 0