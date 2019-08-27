from flask_restful import Resource
from flask import request
from models.users import FoodieUser
from api.schemas.user import NewUserSchema
from api.schemas.auth import LoginSchema
from marshmallow import ValidationError
import models


class NewUser(Resource):

    def post(self):
        try:
            user_data = NewUserSchema().load(request.get_json(force=True))
        except ValidationError as e:
            return e.messages, 400

        email = user_data['email']

        new_user = FoodieUser(**user_data)
        models.Session.add(new_user)
        models.Session.commit()
        user = FoodieUser.get_by_email(email)

        return user.as_dict(), 201



class User(Resource):
    def get(self, id=None):
        if id is None:
            r = models.Session.query(FoodieUser).all()
            return [e.as_dict() for e in r], 200
        else:
            r = models.Session.query(FoodieUser).get(id)
            if r is not None:
                return r.as_dict(), 200
            else:
                return f"User with id {id} was not found", 404
