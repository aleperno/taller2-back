from flask_restful import Resource
from flask import request
from models.users import FoodieUser, AuthToken
from api.schemas.user import NewUserSchema
from api.schemas.auth import LoginSchema, RequiresAuthorization
from marshmallow import ValidationError, EXCLUDE
import models


def requires_auth(func):
    """
    Decora un endpoint solicitando autorizacion

    El header 'Authorization' debe estar presente y ser valido (token de usuario). Con dicho token se obtiene el
    `user_id` que se le pasa como parametro al endpoint que se está decorando
    """
    def inner(*args, **kwargs):
        try:
            auth = RequiresAuthorization(unknown=EXCLUDE).load(dict(request.headers))
        except ValidationError as e:
            return e.messages, 403
        token = auth.get('Authorization')
        user_id = AuthToken.validate_token(token)
        if user_id:
            return func(*args, user_id=user_id, **kwargs)
        else:
            return "Bad Token", 403
    return inner


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
    @requires_auth
    def get(self, user_id):
        r = models.Session.query(FoodieUser).get(user_id)
        if r is not None:
            return r.as_dict(), 200
        else:
            return f"User with id {user_id} was not found", 404
