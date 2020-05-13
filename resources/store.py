from flask_restful import Resource
from flask_jwt_extended import jwt_required, fresh_jwt_required
from sqlalchemy.exc import SQLAlchemyError
from models.store import StoreModel
from schemas.store import StoreSchema

# HTTP Status Codes
from config.constants import OK, CREATED, NOT_FOUND, BAD_REQUEST, INTERNAL_SERVER_ERROR


store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    @jwt_required
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store), OK

        return {"message": "store_not_found"}, NOT_FOUND

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {"message": "store_name_exists" + name}, BAD_REQUEST

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except SQLAlchemyError:
            return {"message": "store_error_inserting"}, INTERNAL_SERVER_ERROR

        return store_schema.dump(store), CREATED

    @classmethod
    @fresh_jwt_required
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "store_deleted"}, OK

        return {"message": "store_not_found"}, NOT_FOUND


class StoreList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return {"stores": store_list_schema.dump(StoreModel.find_all())}, OK
