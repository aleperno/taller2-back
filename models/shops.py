import json
import models
from datetime import timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
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

    def as_dict(self):
        d = self.__dict__
        d.pop('_sa_instance_state')
        if 'creation_date' in d:
            d['creation_date'] = d['creation_date'].isoformat()
        return d

    def _as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "location": self.location,
            "category": self.category,
            "creation_date": self.creation_date.isoformat()
        }


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, ForeignKey('foodie_user.id'))
    name = Column(String)
    description = Column(String)
    category = Column(String)
    price = Column(String)
    creation_date = Column(DateTime, default=utcnow)

    def as_dict(self):
        d = self.__dict__
        d.pop('_sa_instance_state')
        if 'creation_date' in d:
            d['creation_date'] = d['creation_date'].isoformat()
        return d
