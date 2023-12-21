from models.models.user_model import User
from sqlalchemy import insert
from models.setup import db

def add_user_controller(email, phone, password, role_type):
    user = User(email=email, phone_no=phone, password=password, role_type=role_type)
    db.session.add(user)
    db.session.commit()
    return user.id