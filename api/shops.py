from flask_restful import Resource
from models.shops import Product, FoodieShop, Order
from models.users import FoodieUser
from models.deliveries import DeliveryStatus
from models.pricing import PricingEngine
from api.schemas.shops import OrderSchema, ChooseDeliverySchema, CancelOrderSchema, AcceptOrderSchema
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

        deliveries_only = not order.favor
        available_deliveries = DeliveryStatus.get_all_available_distance(shop_location, deliveries_only=deliveries_only)
        """
        for d in available_deliveries:
            distance = d['distance']
            price = PricingEngine.get_distance_price(distance)
            d['price'] = price
        """
        if available_deliveries:
            closest_delivery = min(available_deliveries, key=lambda x: x['distance'])
        price = PricingEngine.get_distance_price(order.distance)
        order.price = price
        order.save_to_db()

        data = {
            'order_id': order.id,
            'available': {x['user_id']: x for x in available_deliveries},
            'closest': closest_delivery['user_id'] if available_deliveries else None,
            'delivery_price': price,
        }
        return data, 200


class OrderStatus(Resource):
    def get(self, order_id):
        order = Order.get_by_id(order_id)
        if not order:
            return "Not found", 404

        if order.status_id <= 1:
            """
            El pedido está en pending o esperando a que un delivery lo acepte
            """
            shop_location = order.shop_location

            deliveries_only = not order.favor

            available_deliveries = DeliveryStatus.get_all_available_distance(shop_location, deliveries_only=deliveries_only)
            """
            for d in available_deliveries:
                distance = d['distance']
                price = PricingEngine.get_distance_price(distance)
                d['price'] = price
            """
            if available_deliveries:
                closest_delivery = min(available_deliveries, key=lambda x: x['distance'])


            data = {
                'available': {x['user_id']: x for x in available_deliveries},
                'closest': closest_delivery['user_id'] if available_deliveries else None,
                'delivery_price': order.price
            }

            if order.status_id == 1:
                if order.delivery_id in data['available']:
                    data['chosen'] = order.delivery_id
                else:
                    order.set_pending()

            data.update({'status_id': order.status_id,
                         'status': order.status})

            return data, 200
        elif order.status_id == 2:
            return order.get_delivery_status()
        elif order.is_cancelled():
            return {'status_id': order.status_id, 'status': order.status}, 200


class ChooseDelivery(Resource):
    @validates_post_schema(ChooseDeliverySchema)
    def post(self, post_data):
        order_id = post_data.get('order_id')
        user_id = post_data.get('user_id')
        delivery_id = post_data.get('delivery_id')

        order = Order.get_by_id(order_id)

        if user_id != order.user_id:
            return "Forbidden", 403

        delivery_status = DeliveryStatus.get_by_id(delivery_id)

        if not delivery_status.is_available:
            return {'status': "Choose another", 'status_id': order.status_id}, 200
        else:
            order.set_chosen_delivery(delivery_id)
            return {'status': "Waiting delivery acceptance", 'status_id': order.status_id}, 200


class CancelOrder(Resource):
    @validates_post_schema(CancelOrderSchema)
    def post(self, order_id, post_data):
        #order_id = post_data.get('order_id')
        user_id = post_data.get('user_id')

        order = Order.get_by_id(order_id)

        if user_id != order.user_id:
            return "Forbidden", 403

        if order.can_cancel():
            order.cancel()
            order.save_to_db()

        return {'status': order.status, 'status_id': order.status_id}, 200


class AvailableOrders(Resource):
    """
    Para que un delivery consulte que órdenes tiene disponible para aceptar
    """
    def get(self, user_id):
        user = FoodieUser.get_by_id(user_id)

        orders = Order.get_available_deliveries(user_id)
        return [order.data_for_delivery() for order in orders], 200


class AcceptOrder(Resource):
    @validates_post_schema(AcceptOrderSchema)
    def post(self, post_data):
        user_id = post_data.get('user_id')
        order_id = post_data.get('order_id')

        user = DeliveryStatus.get_by_id(user_id)
        order = Order.get_by_id(order_id)

        if order.delivery_id != user_id:
            return False, 200
        else:
            order.set_accepted_by_delivery()
            user.set_busy()
            return True, 200