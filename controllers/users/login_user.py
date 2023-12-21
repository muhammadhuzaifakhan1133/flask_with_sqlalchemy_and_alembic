from models.models.user_model import User
from models.setup import db
from sqlalchemy import select

def login_user_controller(email, phone, password):
    query = select(User).where(User.password ==password)
    print(query)
    if phone:
        query = query.where(User.phone_no == phone)
    else:
        query = query.where(User.email == email)
    user = db.session.execute(query).scalar()
    if (user is None): return None, None
    return user.id, user.role_type.value