import models
from datetime import timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from models import Base
from utils import random_string, utcnow

TIMEDELTA = 1

class DeliveryStatus(Base):
    __tablename__ = 'delivery_location'

    user_id = Column(Integer, ForeignKey('foodie_user.id'), primary_key=True)
    location = Column(String)
    available = Column(Boolean)
    last_updated = Column(DateTime, default=utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.available = True
        self.last_updated = utcnow()

    @property
    def expired(self):
        """
        Si la última actualización de una posición fue hace más de una determinada cantidad de tiempo,
        se considera que dicha posición ya no es válida
        """
        return False
        expiration_date = self.last_updated + timedelta(minutes=TIMEDELTA)
        return utcnow() > expiration_date

    def set_busy(self):
        self.available = False
        self.save_to_db()

    def set_free(self):
        self.available = True
        self.save_to_db()

    def update_location(self, location):
        self.location = location
        self.last_updated = utcnow()
        self.save_to_db()

    @property
    def is_available(self):
        return not self.expired and self.available

    @classmethod
    def get_all_available(cls):
        all = cls.get_all()
        available = [x for x in all if x.is_available]
        return [x.as_dict() for x in available]