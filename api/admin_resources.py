from api.resources import api, app # noqa
from api.admin.users import Users
from api.admin.admins import Admins, NewAdmin, ChangePassword
from api.admin.shops import Shops, Products, Orders
from api.auth import AdminLogin
from models.admins import FoodieAdmin


def check_admin_status():
    if not FoodieAdmin.get_all():
        # Need to create a default admin
        admin = FoodieAdmin(email='admin@foodie.com',
                            name='foodie',
                            surname='example',
                            password='admin123')
        admin.save_to_db()


# New Admins
api.add_resource(NewAdmin, "/api/admin/new_admin")

# Auth
api.add_resource(AdminLogin, "/api/admin/login")
api.add_resource(ChangePassword, "/api/admin/change_password")

# Admin Resources
api.add_resource(Admins, "/api/admin/admins")

# Resources
api.add_resource(Users, "/api/admin/users/<int:user_id>")
api.add_resource(Users, "/api/admin/users", endpoint='userss')
api.add_resource(Shops, "/api/admin/shops/<int:shop_id>")
api.add_resource(Shops, "/api/admin/shops", endpoint='shopss')
api.add_resource(Products, "/api/admin/products")
api.add_resource(Orders, "/api/admin/orders")
