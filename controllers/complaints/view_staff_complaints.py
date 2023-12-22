from models.setup import db
from models.models.complaint_model import Complaint
from sqlalchemy import select, Table, Column, Integer, String, MetaData, ForeignKey, Text, DateTime

def view_staff_complaints_controller(status_id, user_id):
    complaints = db.session.query(Complaint).filter(
        Complaint.complaint_status_id == status_id,
        Complaint.assignee_id == user_id
    ).all()
    return [complaint.serialize for complaint in complaints]