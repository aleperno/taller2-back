
from datetime import timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, desc
from models import Base, JSONEncodedValue
from utils import random_string, utcnow


class PricingRules(Base):
    __tablename__ = 'pricing_rule'

    id = Column(Integer, primary_key=True)
    raw_data = Column(JSONEncodedValue)
    last_updated = Column(DateTime, default=utcnow)

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_data = data
        self.last_updated = utcnow()

    @classmethod
    def get_current_rule(cls):
        rule = cls.query().order_by(desc(cls.last_updated)).limit(1).scalar()
        if rule:
            return rule
        else:
            return None

    @classmethod
    def update_rule(cls, data):
        rule = cls.get_current_rule()
        if rule is None:
            new_rule = cls(data=data)
            new_rule.save_to_db()
        else:
            rule.raw_data = data
            rule.save_to_db()


class PricingEngine(object):

    base = 20

    @classmethod
    def get_distance_price(cls, distance):
        if distance < 2000:
            return cls.base
        else:
            extra = distance - 2000
            extra_price = 15 * (extra // 1000)
            return cls.base + extra_price

