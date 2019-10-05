from flask_restful import Resource
from models.shops import Product, FoodieShop


class Shops(Resource):
    def get(self):
        return FoodieShop.get_all()


class ShopProducts(Resource):
    def get(self, shop_id):
        prods = Product.get_shop_products(shop_id)
        return [p.as_dict() for p in prods], 200
