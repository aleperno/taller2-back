from flask_restful import Resource
from flask import request
from models import GlovoUser
from api.schemas.user import NewUserSchema
import models


class NewUser(Resource):

    def post(self):
        errors = NewUserSchema().validate(request.json)
        if errors:
            return errors, 400
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        exists = self.get_user_by_email(email)

        if exists:
            return "Email already registered", 400
        else:
            new_user = GlovoUser(name=name, email=email, password=password)
            models.Session.add(new_user)
            models.Session.commit()
            user = self.get_user_by_email(email)

            return user.as_dict(), 200

    def get_user_by_email(self, email):
        return models.Session.query(GlovoUser).filter(GlovoUser.email==email).scalar()


