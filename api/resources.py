from flask import Flask
from flask_restful import Api
from api.user import NewUser, User
from api.auth import Login, ForgotPassword, ResetPassword, FacebookLogin
from api.shops import ShopProducts, Shops#, Order

app = Flask(__name__)
api = Api(app)

# Authorization Resources
api.add_resource(User, "/api/user")
api.add_resource(NewUser, '/api/new_user')
api.add_resource(Login, '/api/login')
api.add_resource(FacebookLogin, '/api/fb_login')
api.add_resource(ForgotPassword, '/api/forgot_password')
api.add_resource(ResetPassword, '/api/reset_password')

# Shops & Products Resources
api.add_resource(Shops, "/api/shops", endpoint="user_shops")
api.add_resource(ShopProducts, "/api/shops/<int:shop_id>/products")
#api.add_resource(Order, "/api/orders")
