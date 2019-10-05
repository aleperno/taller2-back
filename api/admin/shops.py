from flask_restful import Resource
from api.utils import validates_post_schema
from api.schemas.shops import NewShopSchema
from models.shops import FoodieShop


class Shops(Resource):
    def get(self, shop_id=None):
        if shop_id is None:
            r = FoodieShop.query().all()
            return [e.as_dict() for e in r], 200
        else:
            r = FoodieShop.query().get(shop_id)
            if r is not None:
                return r.as_dict(), 200
            else:
                return f"Shop with id {shop_id} was not found", 404

    @validates_post_schema(NewShopSchema)
    def post(self, post_data):
        new_shop = FoodieShop(**post_data)
        new_shop.save_to_db()

        return new_shop._as_dict(), 200