from flask_restful import Resource
from flask import request
from models import GlovoUser, Session
from api.schemas.user import NewUserSchema

s = Session()

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
            s.add(new_user)
            s.commit()
            user = self.get_user_by_email(email)

            return user.as_dict(), 200

    def get_user_by_email(self, email):
        return s.query(GlovoUser).filter(GlovoUser.email==email).scalar()


