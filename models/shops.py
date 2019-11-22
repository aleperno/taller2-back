from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from models import Base, JSONEncodedValue
from utils import utcnow


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
    favor = Column(Boolean, default=False)
    products = Column(JSONEncodedValue)
    price = Column(Float)
    creation_date = Column(DateTime, default=utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = 'pending'
        self.distance = 445
        self.shop_location = FoodieShop.get_by_id(self.shop_id).location

    def has_finished(self):
        return self.status == 'delivered'


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
