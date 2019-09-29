from flask_restful import Resource
from models.users import FoodieUser
import models


class ListUsers(Resource):
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
