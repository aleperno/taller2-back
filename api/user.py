from flask_restful import Resource
from flask import request
from models.users import FoodieUser
from api.schemas.user import NewUserSchema
from api.utils import validates_post_schema
from api.utils.auth import requires_user_auth
from marshmallow import ValidationError
import models


class NewUser(Resource):
    @validates_post_schema(NewUserSchema)
    def post(self, post_data):
        email = post_data['email']

        new_user = FoodieUser(**post_data)
        models.Session.add(new_user)
        models.Session.commit()
        user = FoodieUser.get_by_email(email)

        return user.as_dict(), 201


class User(Resource):
    @requires_user_auth
    def get(self, user_id):
        r = models.Session.query(FoodieUser).get(user_id)
        if r is not None:
            return r.as_dict(), 200
        else:
            return f"User with id {user_id} was not found", 404
