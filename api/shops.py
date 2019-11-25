from flask_restful import Resource
from models.shops import Product, FoodieShop, Order
from models.deliveries import DeliveryStatus
from api.schemas.shops import OrderSchema
from api.utils.__init__ import validates_post_schema


class Shops(Resource):
    def get(self):
        return FoodieShop.get_all_dict()


class ShopProducts(Resource):
    def get(self, shop_id):
        prods = Product.get_shop_products(shop_id)
        return [p.as_dict() for p in prods], 200


class OrderEndpoint(Resource):
    def get(self):
        return Order.get_all_dict(), 200

    @validates_post_schema(OrderSchema)
    def post(self, post_data):
        order = Order(**post_data)
        order.save_to_db()

        shop_location = order.shop_location

        available_deliveries = DeliveryStatus.get_all_available_distance(shop_location)
        closest_delivery = min(available_deliveries, key=lambda x: x['distance'])

        data = {
            'available': {x['user_id']: x for x in available_deliveries},
            'closest': closest_delivery['user_id']
        }
        return data, 200
