from flask_restful import Resource
from api.utils import validates_post_schema
from api.schemas.admins import NewAdminSchema, ChangePasswordSchema
from api.utils.auth import requires_admin_auth
from models.admins import FoodieAdmin


class NewAdmin(Resource):
    @requires_admin_auth
    @validates_post_schema(NewAdminSchema)
    def post(self, post_data, **kw):
        email = post_data['email']

        new_adm = FoodieAdmin(**post_data)
        new_adm.save_to_db()

        return new_adm.as_dict(), 201


class ChangePassword(Resource):
    @requires_admin_auth
    @validates_post_schema(ChangePasswordSchema)
    def put(self, post_data, admin_id):
        admin = FoodieAdmin.get_by_id(admin_id)
        pwd = post_data['password']

        admin.change_password(pwd)
        admin.save_to_db()

        return 'ok', 200
