from .login_user import login_user_bp
from .add_user import add_user_bp
from .update_user import update_user_bp
from .delete_user import delete_user_bp

users_router_list = []
users_router_list.append(login_user_bp)
users_router_list.append(add_user_bp)
users_router_list.append(update_user_bp)
users_router_list.append(delete_user_bp)