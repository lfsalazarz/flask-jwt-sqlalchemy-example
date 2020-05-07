from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
import traceback
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
# HTTP Status Codes
from config.constants import OK, CREATED, NOT_FOUND, BAD_REQUEST, INTERNAL_SERVER_ERROR, UNAUTHORIZED

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        print(user)

        if UserModel.find_by_username(user.username):
            return {"message": gettext("user_username_exists")}, BAD_REQUEST

        if UserModel.find_by_email(user.email):
            return {"message": gettext("user_email_exists")}, BAD_REQUEST

        try:
            user.save_to_db()
            return {"message": "user_registered"}, CREATED
        except:  # failed to save user to db
            traceback.print_exc()
            user.delete_from_db()  # rollback
            return {"message": "user_error_creating"}, INTERNAL_SERVER_ERROR


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user_not_found"}, NOT_FOUND

        return user_schema.dump(user), OK

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user_not_found"}, NOT_FOUND

        user.delete_from_db()
        return {"message": "user_deleted"}, OK


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email",))

        user = UserModel.find_by_username(user_data.username)

        if user and safe_str_cmp(user.password, user_data.password):
            access_token = create_access_token(user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return (
                {"access_token": access_token, "refresh_token": refresh_token},
                OK,
            )

        return {"message": "user_invalid_credentials"}, UNAUTHORIZED


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": "user_logged_out" + user_id}, OK


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, OK
