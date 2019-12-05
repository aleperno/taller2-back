from flask_restful import Resource
from models.users import FoodieUser
from api.utils import validates_post_schema
from api.schemas.admins import EditUserSchema
from api.validators import email_not_existing
from marshmallow import ValidationError
from utils.logging import MyLogger
import models


class Users(Resource):
    def get(self, user_id=None):
        if user_id is None:
            r = models.Session.query(FoodieUser).all()
            return [e.as_dict() for e in r], 200
        else:
            r = models.Session.query(FoodieUser).get(user_id)
            if r is not None:
                return r.as_dict(), 200
            else:
                return f"User with id {user_id} was not found", 404

    @validates_post_schema(EditUserSchema)
    def put(self, user_id, post_data):
        user = FoodieUser.get_by_id(user_id)
        if not user:
            return f"User with id {user_id} was not found", 404

        new_email = post_data.get('email')
        try:
            if new_email and new_email != user.email:
                email_not_existing(new_email)

            user.update_from_dict(**post_data)

            if user.is_delivery and not user.photo_url:
                return {'photo_url': ["Delivery user must have photo"]}, 400
        except ValidationError as e:
            return e.messages, 400

        user.save_to_db()
        return user.as_dict(), 200

    def delete(self, user_id):
        MyLogger.info("Se inhabilitó al user %d", user_id)
        user = FoodieUser.get_by_id(user_id)
        user.active = False
        user.save_to_db()

        return user.as_dict(), 200

