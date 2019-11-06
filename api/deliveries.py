from flask_restful import Resource
from flask import request
from models.users import FoodieUser
from api.schemas.user import NewUserSchema
from api.utils import validates_post_schema
from api.schemas.deliveries import DeliveryStatusSchema
from models.deliveries import DeliveryStatus
from api.utils.auth import requires_user_auth
from marshmallow import ValidationError
import models


class DeliveryStatusResource(Resource):
    def get(self):
        return DeliveryStatus.get_all_dict(), 200

    @validates_post_schema(DeliveryStatusSchema)
    def post(self, post_data):
        delivery_id = post_data.get('user_id')
        location = post_data.get('location')
        available = post_data.get('available')

        current = DeliveryStatus.get_by_id(delivery_id)
        if not current:
            new = DeliveryStatus(**post_data)
            new.save_to_db()
            return new.as_dict(), 201
        else:
            current.update_location(location)
            if available:
                current.set_free()
            return current.as_dict(), 200


class AvailableDeliveries(Resource):
    def get(self):
        available = DeliveryStatus.get_all_available()
        for delivery in available:
            user = FoodieUser.get_by_id(delivery.get('user_id'))
            delivery.update(user.public_info())

        return available, 200
