from flask_restful import Resource
from flask import request
from models.users import FoodieUser, AuthToken, PasswordRecoveryToken
from api.schemas.auth import LoginSchema, ForgottenPasswordSchema
from utils.mail import send_token_to_mail
from marshmallow import ValidationError
import models


class Login(Resource):
    def post(self):
        try:
            user_data = LoginSchema().load(request.get_json(force=True))
        except ValidationError as e:
            return e.messages, 400

        email = user_data['email']
        password = user_data['password']

        user = FoodieUser.get_by_email(email)

        if not user:
            return 'User not found', 404
        elif not user.valid_password(password):
            return 'Wrong Password', 401
        else:
            return AuthToken.get_user_token(user.id)._as_dict(), 200


class ForgotPassword(Resource):
    def post(self):
        try:
            user_email = ForgottenPasswordSchema().load(request.get_json(force=True))
        except ValidationError as e:
            return e.messages, 400

        user = FoodieUser.get_by_email(user_email['email'])

        token = PasswordRecoveryToken.get_user_token(user.id)
        send_token_to_mail(token.token, user.email, token.expiration)
        return token.token, 200
