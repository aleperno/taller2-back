from flask import request
from flask_restful import Resource
from api.utils import validates_post_schema, AdminResource
from api.schemas.admins import NewAdminSchema, ChangePasswordSchema
from models.admins import FoodieAdmin


class Admins(AdminResource):

    def get(self, *args, **kwargs):
        raw_admin_ids = request.args.get('admin_id')
        if raw_admin_ids:
            ids = raw_admin_ids.split(',')
            admins = FoodieAdmin.get_by_ids(ids)
        else:
            admins = FoodieAdmin.get_all()

        return [adm.as_dict() for adm in admins], 200

    @validates_post_schema(NewAdminSchema)
    def post(self, post_data, **kw):
        email = post_data['email']

        new_adm = FoodieAdmin(**post_data)
        new_adm.save_to_db()

        return new_adm.as_dict(), 201

    @validates_post_schema(ChangePasswordSchema)
    def put(self, post_data, admin_id):
        admin = FoodieAdmin.get_by_id(admin_id)
        pwd = post_data['password']

        admin.change_password(pwd)
        admin.save_to_db()

        return 'ok', 200

"""
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
"""
