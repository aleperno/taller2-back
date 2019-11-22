from flask_restful import Resource
from models.shops import Product, FoodieShop, Order, OrderReview
from api.schemas.shops import OrderSchema, OrderReviewSchema
from api.utils.__init__ import validates_post_schema
from models.users import FoodieUser


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
        return 'Ok', 200


class OrderReviewEndpoint(Resource):
    @validates_post_schema(OrderReviewSchema)
    def post(self, post_data):
        order_id = post_data.get('order_id')
        user_id = post_data.get('user_id')
        review = post_data.get('review')

        order = Order.get_by_id(order_id)

        if not (order.user_id == user_id or order.delivery_id == user_id):
            """
            The user wanting to perform the action, is not the user nor the delivery of the order.
            Therefore should not be able to add a review to the order.
            """
            return {'user_id': ["User is not allowed to perform the action"]}, 403

        if not order.has_finished():
            return "Order must be finished before performing a review", 400

        user = FoodieUser.get_by_id(user_id)
        """
        El usuario puede ser tanto el `cliente` como el `delivery` de una orden, independientemente de su rol de usuario
        Por ejemplo, en una orde que es un favor, tanto el `cliente` como el `delivery` pueden ser usuarios.
        """
        review_role = 'delivery' if user_id == order.user_id else 'user'

        order_review = OrderReview.get_by_id(order.id)

        if not order_review:
            order_review = OrderReview.new_review(order_id=order.id, role=review_role, review=review)
        else:
            current_review = order_review.get_role_review(review_role)

            if current_review is not None:
                return "The order has already a review", 400
            else:
                order_review.add_user_review(review_role, review)
        return 'Ok', 200




