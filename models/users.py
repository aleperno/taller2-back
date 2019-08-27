import json

from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.types import TypeDecorator, VARCHAR
from models import Base


class JSONEncodedValue(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class FoodieUser(Base):
    __tablename__ = 'foodie_user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    role = Column(String)
    subscription = Column(String)
    password = Column(String)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'phone': self.phone,
            'password': self.password,
            'role': self.role,
            'subscription': self.subscription,
        }

    def is_premium(self):
        return self.subscription == 'premium'

    def is_user(self):
        return self.role == 'user'

    def __repr__(self):
        return f'Foodie User: id: {self.id}, name: {self.name}'
