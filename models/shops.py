from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from models import Base, JSONEncodedValue
from utils import utcnow
from utils.maps import distance_between
from copy import copy

PENDING = 0
WAITING_DELIVERY_ACCEPTANCE = 1
DELIVERY_ACCEPTED = 2
CANCELLED = 9

class FoodieShop(Base):
    __tablename__ = 'foodie_shop'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)
    location = Column(String)
    category = Column(String)
    creation_date = Column(DateTime, default=utcnow)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, ForeignKey('foodie_shop.id'))
    name = Column(String)
    description = Column(String)
    category = Column(String)
    price = Column(Float)
    creation_date = Column(DateTime, default=utcnow)

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

    def can_cancel(self):
        """
        Solo se puede cancelar el pedido si el mismo se encuentra en `pending` o `waiting_delivery_acceptance`
        """
        return self.status_id <= 1

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
        return self.as_dict()
