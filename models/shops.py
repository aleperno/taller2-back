from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from models import Base, JSONEncodedValue
from models.pricing import PricingEngine
from utils import utcnow
from utils.maps import distance_between
from copy import copy

PENDING = 0
WAITING_DELIVERY_ACCEPTANCE = 1
DELIVERY_ACCEPTED = 2
IN_SHOP = 3
OUT_SHOP = 4
DELIVERED = 5
CONFIRMED = 6
CANCELLED = 9

STATUS_MAP = {
    'accepted': 2,
    'in_shop': 3,
    'out_shop': 4,
    'delivered': 5,
}

class FoodieShop(Base):
    __tablename__ = 'foodie_shop'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)
    location = Column(String)
    category = Column(String)
    creation_date = Column(DateTime, default=utcnow)
    active = Column(Boolean, default=True)

    def has_products(self):
        prods = Product.get_shop_products(self.id)
        return False if not prods else True


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, ForeignKey('foodie_shop.id'))
    name = Column(String)
    description = Column(String)
    category = Column(String)
    price = Column(Float)
    creation_date = Column(DateTime, default=utcnow)
    active = Column(Boolean, default=True)

    @classmethod
    def get_shop_products(cls, shop_id):
        return cls.query().filter(cls.shop_id==shop_id).all()

    @classmethod
    def product_belongs_shop(cls, product_id, shop_id):
        """
        Returns if a given product belongs to a given shop
        """
        product = cls.query().get(product_id)
        if product:
            return product.shop_id == shop_id
        else:
            return False


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, ForeignKey('foodie_shop.id'))
    user_id = Column(Integer, ForeignKey('foodie_user.id'))
    delivery_id = Column(Integer, ForeignKey('foodie_user.id'))
    user_location = Column(String)
    shop_location = Column(String)
    distance = Column(Integer)
    status = Column(String)
    status_id = Column(Integer)
    favor = Column(Boolean, default=False)
    products = Column(JSONEncodedValue)
    price = Column(Float)
    product_prices = Column(Float)
    creation_date = Column(DateTime, default=utcnow)
    order_metadata = Column(JSONEncodedValue)
    delivery_revenue = Column(Float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = 'pending'
        self.status_id = PENDING
        self.shop_location = FoodieShop.get_by_id(self.shop_id).location
        dist = distance_between([self.shop_location], self.user_location)
        self.distance = dist[0]['distance']
        self.order_metadata = {
            'creation_date': utcnow().isoformat(),
        }
        self.set_product_prices()

    def set_product_prices(self):
        sum = 0
        for product in self.products:
            count = product['quantity']
            _id = product['id']
            prod = Product.get_by_id(_id)
            sum += (count * prod.price)
        self.product_prices = sum

    def update_metadata(self, key):
        meta = copy(self.order_metadata)
        meta[key] = utcnow().isoformat()
        self.order_metadata = meta

    def set_chosen_delivery(self, delivery_id):
        self.delivery_id = delivery_id
        self.status = 'pending_delivery_acceptance'
        self.status_id = WAITING_DELIVERY_ACCEPTANCE
        self.update_metadata('pending_delivery_acceptance')
        self.save_to_db()

    def set_pending(self):
        self.status = 'pending'
        self.delivery_id = None
        self.status_id = PENDING
        self.save_to_db()

    def set_status(self, new_status):
        new_status_id = STATUS_MAP[new_status]
        if new_status_id not in (self.status_id, self.status_id + 1):
            """
            El cambio de estado se acepta cuando el status_id es el mismo (idempotente)
            o un estado inmediatamente anterior. No se aceptan saltos de estado.
            """
            return False
        else:
            if new_status_id == DELIVERY_ACCEPTED:
                price = self.get_delivery_price()
                self.delivery_revenue = price
            self.status_id = new_status_id
            self.status = new_status
            self.update_metadata(new_status)
            self.save_to_db()
            return True

    def can_cancel(self):
        """
        Solo se puede cancelar el pedido si el mismo se encuentra en `pending` o `waiting_delivery_acceptance`
        """
        return self.status_id <= WAITING_DELIVERY_ACCEPTANCE

    def cancel(self):
        self.status = 'cancelled'
        self.status_id = CANCELLED
        self.update_metadata('cancelled')

    def is_cancelled(self):
        return self.status_id == CANCELLED

    @classmethod
    def get_available_deliveries(cls, delivery_id):
        return Order.query().filter(Order.delivery_id==delivery_id, Order.status_id==1).all()

    def data_for_delivery(self):
        from models.deliveries import DeliveryStatus
        from models.users import FoodieUser
        keys = ['id', 'shop_location', 'user_location', 'shop_id', 'user_id', 'distance', 'favor']

        status = DeliveryStatus.get_by_id(self.delivery_id)
        distance = status.distance_to(self.shop_location)['distance']

        data = {k:v for k,v in self.as_dict().items() if k in keys}
        data['distance_to_shop'] = distance
        data['total_distance'] = distance + self.distance
        user = FoodieUser.get_by_id(self.user_id)
        data['user_data'] = user.public_info()
        data['revenue'] = self.get_delivery_price()
        return data

    def get_delivery_status(self):
        from models.deliveries import DeliveryStatus
        from models.users import FoodieUser
        status = DeliveryStatus.get_by_id(self.delivery_id)
        user = FoodieUser.get_by_id(self.delivery_id)
        location = status.location
        return {
            'status': self.status,
            'status_id': self.status_id,
            'delivery_location': location,
            'delivery_data': user.public_info(),
        }

    def get_delivery_price(self):
        return PricingEngine.get_delivery_revenue(self, self.delivery_id)

    def confirm_delivery(self):
        from models.users import FoodieUser
        user = FoodieUser.get_by_id(self.user_id)
        delivery = FoodieUser.get_by_id(self.delivery_id)

        if self.favor:
            user.update_favor_balance(-self.price)
            delivery.update_favor_balance(self.delivery_revenue)
        else:
            user.update_cash_balance(-self.price)
            delivery.update_cash_balance(self.delivery_revenue)

        self.status_id = CONFIRMED
        self.status = 'confirmed'
        self.update_metadata('confirmed')
        self.save_to_db()

    def has_finished(self):
        return self.status_id == CONFIRMED


class OrderReview(Base):
    __tablename__ = 'orders_review'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    user_review = Column(Float)
    delivery_review = Column(Float)

    @classmethod
    def new_review(cls, order_id, role, review):
        order_review = cls.get_by_id(order_id)
        key = f'{role}_review'

        data = {
            'order_id': order_id,
            key: review
        }
        if not order_review:
            order_review = cls(**data)
        else:
            setattr(order_review, key, review)
        order_review.save_to_db()

    @property
    def order(self):
        return Order.get_by_id(self.order_id)

    def add_user_review(self, role, review):
        self.new_review(self.order_id, role, review)

    def get_role_review(self, role):
        return getattr(self, f'{role}_review')
