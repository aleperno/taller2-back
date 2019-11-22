from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from api.user import NewUser, User
from api.auth import UserLogin, ForgotPassword, ResetPassword, FacebookLogin
from api.shops import ShopProducts, Shops, OrderEndpoint, OrderReviewEndpoint
from api.deliveries import DeliveryStatusResource, AvailableDeliveries

app = Flask(__name__)
CORS(app)
api = Api(app)


# Authorization Resources
api.add_resource(User, "/api/user")
api.add_resource(NewUser, '/api/new_user')
api.add_resource(UserLogin, '/api/login')
api.add_resource(FacebookLogin, '/api/fb_login')
api.add_resource(ForgotPassword, '/api/forgot_password')
api.add_resource(ResetPassword, '/api/reset_password')

# Shops & Products Resources
api.add_resource(Shops, "/api/shops", endpoint="user_shops")
api.add_resource(ShopProducts, "/api/shops/<int:shop_id>/products")
api.add_resource(OrderEndpoint, "/api/orders")

api.add_resource(OrderReviewEndpoint, "/api/orders/review")


# Deliveries
api.add_resource(DeliveryStatusResource, "/api/deliveries/status")
api.add_resource(AvailableDeliveries, "/api/deliveries/available")
