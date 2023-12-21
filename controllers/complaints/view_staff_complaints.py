from models.setup import db
from models.models.complaint_model import Complaint
from sqlalchemy import select, Table, Column, Integer, String, MetaData, ForeignKey, Text, DateTime

def view_staff_complaints_controller(status_id, user_id):
    print(status_id, user_id)
    keys = ["id", "title", "description", "file_url", "complaint_type_id", "complaint_status_id", "assignee_id", "created_at"]
    complaint_table = Table(
     "complaint",
     MetaData(),
     Column(keys[0], Integer, primary_key=True),
     Column(keys[1], String),
     Column(keys[2], Text),
     Column(keys[3], Text),
     Column(keys[4], ForeignKey('user.id'),),
     Column(keys[5], ForeignKey('user.id'),),
     Column(keys[6], ForeignKey('user.id'),),
     Column(keys[7], DateTime),
 )
    query = select(complaint_table).where(
        complaint_table.c.complaint_status_id == status_id,
        complaint_table.c.assignee_id == user_id
    )
    complaints = db.session.execute(query).all()
    data = []
    for row in complaints:
        print(row)
        c ={}
        for k, v in zip(keys, row):
            print(k,v)
            c[k]=v
        data.append(c.copy())
    return data