from flask_restful import Resource
from flask import request
from models.users import FoodieUser
from api.schemas.user import NewUserSchema
from marshmallow import ValidationError
import models


class NewUser(Resource):

    def post(self):
        try:
            user_data = NewUserSchema().load(request.json)
        except ValidationError as e:
            return e.messages, 400

        email = user_data['email']

        exists = self.get_user_by_email(email)

        if exists:
            return "Email already registered", 400
        else:
            new_user = FoodieUser(**user_data)
            models.Session.add(new_user)
            models.Session.commit()
            user = self.get_user_by_email(email)

            return user.as_dict(), 200

    def get_user_by_email(self, email):
        return models.Session.query(FoodieUser).filter(FoodieUser.email == email).scalar()


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

