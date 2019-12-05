from flask_restful import Resource
from flask import request
from api.utils.__init__ import validates_post_schema
from api.schemas.shops import NewShopSchema, EditShopSchema, NewProductSchema, EditProductSchema
from models.shops import FoodieShop, Product, Order
from utils.custom_logging import MyLogger


class Shops(Resource):
    def get(self, shop_id=None):
        if shop_id is None:
            MyLogger.info("Admin pide todos los shops")
            r = FoodieShop.query().all()
            return [e.as_dict() for e in r], 200
        else:
            MyLogger.info("Admin pide por el shop %d", shop_id)
            r = FoodieShop.query().get(shop_id)
            if r is not None:
                return r.as_dict(), 200
            else:
                return f"Shop with id {shop_id} was not found", 404

    @validates_post_schema(NewShopSchema)
    def post(self, post_data):
        new_shop = FoodieShop(**post_data)
        new_shop.save_to_db()
        return new_shop.as_dict(), 201

    @validates_post_schema(EditShopSchema)
    def put(self, post_data):
        shop_id = post_data.pop('id')
        shop = FoodieShop.get_by_id(shop_id)
        for k, v in post_data.items():
            setattr(shop, k, v)
        shop.save_to_db()

        return shop.as_dict(), 200

    def delete(self, shop_id):
        MyLogger.info("Se inhabilitó el shop %d", shop_id)
        shop = FoodieShop.get_by_id(shop_id)
        shop.active = False
        shop.save_to_db()
        return shop.as_dict(), 200



class Products(Resource):
    # TODO: Hacer esto bien, tomando los optional args
    def get(self):
        shop_id = request.args.get('shop_id')
        product_id = request.args.get('product_id')
        """
        if shop_id is None and product_id is None:
            r = Product.query().all()
            return [e.as_dict() for e in r], 200
        elif shop_id is not None and product_id is None:
            pass
        else:
            r = FoodieShop.query().get(shop_id)
            if r is not None:
                return r.as_dict(), 200
            else:
                return f"Shop with id {shop_id} was not found", 404
        """
        r = Product.get_all()
        return [e.as_dict() for e in r], 200

    @validates_post_schema(NewProductSchema)
    def post(self, post_data):
        new_shop = Product(**post_data)
        new_shop.save_to_db()

        return new_shop.as_dict(), 201

    @validates_post_schema(EditProductSchema)
    def put(self, post_data):
        product_id = post_data.pop('id')
        product = Product.get_by_id(product_id)
        for k, v in post_data.items():
            setattr(product, k, v)
        product.save_to_db()

        return product.as_dict(), 200

    def delete(self, product_id):
        MyLogger.info("Se inhabilitó el producto %d", product_id)
        product = Product.get_by_id(product_id)
        product.active = False
        product.save_to_db()
        return product.as_dict(), 200


class Orders(Resource):
    def get(self):
        MyLogger.info("Admin pide datos de las órdenes")
        orders = Order.get_all()
        data = []
        for order in orders:
            d = order.as_dict()
            if order.is_accepted():
                delivery_data = order.get_delivery_status()
                d['delivery_location'] = delivery_data['delivery_location']
            data.append(d)

        return data, 200
