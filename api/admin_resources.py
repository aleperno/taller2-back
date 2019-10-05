from api.resources import api, app # noqa
from api.admin.users import ListUsers
from api.admin.shops import Shops, Products


api.add_resource(ListUsers, "/api/admin/users/<int:user_id>")
api.add_resource(ListUsers, "/api/admin/users", endpoint='users')
api.add_resource(Shops, "/api/admin/shops/<int:shop_id>")
api.add_resource(Shops, "/api/admin/shops", endpoint='shopss')
api.add_resource(Products, "/api/admin/products")