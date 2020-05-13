# Standard library imports
import os

# Flask imports
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from dotenv import load_dotenv
from marshmallow import ValidationError

# from werkzeug.exceptions import HTTPException
from db import db
from ma import ma
from blacklist import BLACKLIST

# Resources imports
from resources.user import UserRegister, UserLogin, User, UserLogout
from resources.user import TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# HTTP Status Codes
from config.constants import UNAUTHORIZED, BAD_REQUEST


load_dotenv(".env")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGHT"] = 3 * 1024 * 1024
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
# https://flask-jwt-extended.readthedocs.io/en/latest/options.html
app.secret_key = os.environ.get("APP_SECRET_KEY")
# https://pyjwt.readthedocs.io/en/latest/algorithms.html
app.config["JWT_ALGORITHM"] = "RS256"
app.config["JWT_PUBLIC_KEY"] = open("./certs/pubkey.pem").read()
app.config["JWT_PRIVATE_KEY"] = open("./certs/localhost.key").read()
api = Api(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)
jwt = JWTManager(app)

# @app.after_request
# def after_request(response):
#   response.headers.add("Access-Control-Allow-Origin", "*")
#   response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
#   response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
#   return response


@app.before_first_request
def create_tables():
    db.create_all()


# https://flask.palletsprojects.com/en/1.1.x/errorhandling/#registering
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), BAD_REQUEST


# @app.errorhandler(HTTPException)
# def handle_exception(e):
#     """Return JSON instead of HTML for HTTP errors."""
#     # start with the correct headers and status code from the error
#     response = e.get_response()
#     # replace the body with JSON
#     response.data = json.dumps({
#         "code": e.code,
#         "name": e.name,
#         "description": e.description,
#     })
#     response.content_type = "application/json"
#     return response


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    return {"user_claims_loader": "value"}


# https://flask-jwt-extended.readthedocs.io/en/latest/changing_default_behavior.html#changing-callback-functions
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "message": "Signature verification failed.",
        "error": "invalid_token"
    }), UNAUTHORIZED


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        "error": "authorization_required"
    }), UNAUTHORIZED

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "message": "The token has expired.",
        "error": "token_expired"
    }), UNAUTHORIZED

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        "error": "fresh_token_required"
    }), UNAUTHORIZED

# @jwt.revoked_token_loader
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
