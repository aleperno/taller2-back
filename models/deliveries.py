import models
import random
from datetime import timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from models import Base
from utils.maps import distance_between
#
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

    def distance_to(self, location):
        """
        TODO: Devolver distancia entre self.location y location
        """
        return random.randint(0, 2000)

    @classmethod
    def get_all_available(cls):
        all = cls.get_all()
        available = [x for x in all if x.is_available]
        return available

    @classmethod
    def get_all_available_distance(cls, shop_location):
        from models.users import FoodieUser
        """
        Obtengo todos los deliveries que se encuentan disponibles, junto con la distancia hacia la ubicación
        """
        available = cls.get_all_available()
        locations = [x.location for x in available]
        distances = distance_between(locations, shop_location)

        data = []
        for pos, delivery in enumerate(available):
            distance_data = distances[pos]
            if distance_data['status'] is False:
                # Hay un problema con la ubicacion del delivery
                continue
            else:
                distance = distance_data['distance']
                d = delivery.as_dict()
                user = FoodieUser.get_by_id(delivery.user_id)
                d.update(user.public_info())
                d['distance'] = distance
                data.append(d)
        return data

