from models.setup import db
from models.models.complaint_type_model import ComplaintType


def add_complaint_type_controller(name):
    complaintType = ComplaintType(name=name)
    db.session.add(complaintType)
    db.session.commit()
    return complaintType.id