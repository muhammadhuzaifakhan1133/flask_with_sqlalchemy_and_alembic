from models.setup import db
from models.models.user_model import User
from models.models.complaint_status_model import ComplaintStatus
from models.models.complaint_model import Complaint
from sqlalchemy import select, update, Table, Column, Integer, String, MetaData, ForeignKey

def assign_complaint_controller(complaint_id, user_id):
    user_id = db.session.execute(select(User.id).where(
        User.role_type=="staff",
        User.id==user_id,
        User.is_active=="1",
    )).scalar()
    if (user_id is None): return False
    status_query = select(ComplaintStatus.id).where(ComplaintStatus.name=="ASSIGNED")
    status_id = db.session.execute(status_query).scalar()
    print(user_id, status_id, complaint_id)
    complaint_table = Table(
     "complaint",
     MetaData(),
     Column("id", Integer, primary_key=True),
     Column("assignee_id", ForeignKey('user.id'),),
     Column("complaint_status_id", ForeignKey('complaint_status.id')),
 )
    query = update(complaint_table).where(complaint_table.c.id==complaint_id).values(
            assignee_id=user_id, 
            complaint_status_id=status_id
            )
    result = db.session.execute(query)
    db.session.commit()
    return result.rowcount > 0