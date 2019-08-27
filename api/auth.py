from flask_restful import Resource
from flask import request
from models.users import FoodieUser, AuthToken
from api.schemas.auth import LoginSchema
from marshmallow import ValidationError
import models


class Login(Resource):
    def post(self):
        try:
            user_data = LoginSchema().load(request.json)
        except ValidationError as e:
            return e.messages, 400

        email = user_data['email']
        password = user_data['password']

        user = models.Session.query(FoodieUser).filter(FoodieUser.email==email).scalar()

        if not user:
            return 'User not found', 404
        elif not user.valid_password(password):
            return 'Wrong Password', 403
        else:
            return 'Success', 200
