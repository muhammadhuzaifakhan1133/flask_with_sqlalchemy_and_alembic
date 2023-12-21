from models.models.user_model import User
from models.setup import db
from sqlalchemy import update

def update_user_controller(id, email, phone, password, role_type):
    query = update(User).where(User.id == id)
    if email:
        query = query.values(email=email)
    if phone:
        query = query.values(phone_no=phone)
    if password:
        query = query.values(password=password)
    if role_type:
        query = query.values(role_type=role_type)
    result = db.session.execute(query)
    db.session.commit()
    return result.rowcount > 0