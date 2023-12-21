from models.models.user_model import User
from models.setup import db
from sqlalchemy import delete

def delete_user_controller(id):
    query = delete(User).where(User.id == id)
    result = db.session.execute(query)
    db.session.commit()
    return result.rowcount > 0