
from datetime import timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, desc
from models import Base, JSONEncodedValue
from utils import random_string, utcnow

class PricingRules(Base):
    __tablename__ = 'pricing_rule'

    id = Column(Integer, primary_key=True)
    raw_data = Column(JSONEncodedValue)
    last_updated = Column(DateTime, default=utcnow)

    default_rule = {
        'flat_min_km': 2,
        'flat_base': 20,
        'flat_extra_km': 15,
        'premium_min_km': 3,
        'premium_base': 20,
        'premium_extra_km': 12,
        'delivery_revenue_perc': 85
    }

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

    @classmethod
    def check_initial_status(cls):
        if cls.get_current_rule() is None:
            cls.update_rule(cls.default_rule)

    def get_rules_dict(self):
        return self.raw_data


class PricingEngine(object):

    flat_base = 20
    premium_base = 10

    flat_extra = 15
    premium_extra = 12

    @classmethod
    def get_distance_price(cls, distance, user):
        rules = PricingRules.get_current_rule().get_rules_dict()
        prefix = user.subscription

        base = rules[f'{prefix}_base']
        if distance < (3 * rules[f'{prefix}_min_km']):
            return base
        else:
            extra_mult = rules[f'{prefix}_extra_km']
            extra_km = (distance - 2000) // 1000
            extra_price = extra_mult * extra_km
            return base + extra_price

    @classmethod
    def get_delivery_revenue(cls, order, delivery):
        rules = PricingRules.get_current_rule().get_rules_dict()
        return order.price * (rules['delivery_revenue_perc'] / 100)

