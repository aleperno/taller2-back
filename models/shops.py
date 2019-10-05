import json
import models
from datetime import timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.types import TypeDecorator, VARCHAR
from models import Base
from utils import random_string, utcnow


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
    shop_id = Column(Integer, ForeignKey('foodie_user.id'))
    name = Column(String)
    description = Column(String)
    category = Column(String)
    price = Column(Float)
    creation_date = Column(DateTime, default=utcnow)

    @classmethod
    def get_shop_products(cls, shop_id):
        return cls.query().filter(cls.shop_id==shop_id).all()
