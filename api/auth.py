from flask_restful import Resource
from flask import request
from models.users import FoodieUser, AuthToken, PasswordRecoveryToken, FirebaseToken
from models.admins import FoodieAdmin, AdminAuthToken
from api.schemas.auth import (LoginSchema,
                              ForgottenPasswordSchema,
                              ResetPasswordSchema,
                              FacebookLoginSchema,
                              )
from api.utils.__init__ import validates_post_schema, facebook_get_email
from utils.mail import send_token_to_mail
from marshmallow import ValidationError


class UserLogin(Resource):

    token_cls = AuthToken
    user_cls = FoodieUser

    @validates_post_schema(LoginSchema)
    def post(self, post_data):
        user_data = post_data
        email = user_data['email']
        password = user_data['password']

        user = self.user_cls.get_by_email(email)

        if not user:
            return 'User not found', 404
        elif not user.valid_password(password):
            return 'Wrong Password', 401
        elif not user.active:
            return 'User was disabled', 404
        else:
            firebase_token = post_data.get('firebase_token')
            if firebase_token:
                FirebaseToken.set_token(user.id, firebase_token)
            token = self.token_cls.get_user_token(user.id)._as_dict()
            return token, 200, {'Authorization': token['token']}


class AdminLogin(UserLogin):
    token_cls = AdminAuthToken
    user_cls = FoodieAdmin


class FacebookLogin(Resource):
    @validates_post_schema(FacebookLoginSchema)
    def post(self, post_data):
        access_token = post_data['fb_access_token']

        email = facebook_get_email(access_token)

        if not email:
            # Puede que el token sea invalido
            return "Token invalido", 400

        user = FoodieUser.get_by_email(email)
        if not user:
            return "Usuario inexistente", 404
        
        firebase_token = post_data.get('firebase_token')
        if firebase_token:
            FirebaseToken.set_token(user.id, firebase_token)

        return AuthToken.get_user_token(user.id)._as_dict(), 200


class ForgotPassword(Resource):
    def post(self):
        try:
            user_email = ForgottenPasswordSchema().load(request.get_json(force=True))
        except ValidationError as e:
            return e.messages, 400

        user = FoodieUser.get_by_email(user_email['email'])

        token = PasswordRecoveryToken.generate_token(user.id)
        send_token_to_mail(token.token, user.email, token.expiration)
        return token.token, 200


class ResetPassword(Resource):
    @validates_post_schema(ResetPasswordSchema)
    def post(self, post_data):
        user = FoodieUser.get_by_email(post_data['email'])
        token = post_data['token']
        password = post_data['password']

        if not PasswordRecoveryToken.validate_user_token(user.id, token):
            return 'Invalid Token', 403
        else:
            token_obj = PasswordRecoveryToken.get_user_token(user.id)
            user.password = password
            token_obj.used = True

            user.save_to_db()
            token_obj.save_to_db()

            return 'Password Changed', 200
