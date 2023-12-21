from flask import Flask
import models
from datetime import timedelta
from flask_jwt_extended import JWTManager
from routes.users import users_router_list
from routes.complaints import complaints_router_list
from routes.dashboards import dashboards_router_list
from services.file_services import UPLOAD_FOLDER
from services.response_services import display_response

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost/complaint_management_system"
models.db.init_app(app)


app.secret_key = "o.=1A=e'$FH6S^EL;lQAQRa=5;w{{NlcuVOBpvkL^&2cQTYq)u"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config["JWT_SECRET_KEY"] = "o.=1A=e'$FH6S^EL;lQAQRa=5;w{{NlcuVOBpvkL^&2cQTYq)u"  # Change this!
app.config["JWT_TOKEN_LOCATION"] = ["headers"] # specifying the location of JWT 
app.config["JWT_ALGORITHM"] = "HS256" # symmetric keyed hashing algorithm
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)

@jwt.invalid_token_loader
def invalid_token_callback(jwt_payload):
    return display_response(status_code=400, errors=["Invalid Token"])

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return display_response(status_code=400, errors=["Expired Token"])

@jwt.unauthorized_loader
def unauthorized_callback(jwt_payload):
    return display_response(status_code=400, errors=["Token is required"])

for route in users_router_list:
    app.register_blueprint(route)

for route in complaints_router_list:
    app.register_blueprint(route)

for route in dashboards_router_list:
    app.register_blueprint(route)


if __name__ == "__main__":
    app.run(debug=True)

