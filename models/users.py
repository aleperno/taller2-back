import json
import models
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.types import TypeDecorator, VARCHAR
from models import Base
from utils import random_string


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

    def valid_password(self, password):
        return self.password == password

    @classmethod
    def get_by_email(cls, email):
        return models.Session.query(FoodieUser).filter(FoodieUser.email == email).scalar()

    def __repr__(self):
        return f'Foodie User: id: {self.id}, name: {self.name}'


class AuthToken(Base):
    __tablename__ = 'auth_token'

    user_id = Column(Integer, ForeignKey('foodie_user.id'), primary_key=True)
    token = Column(String, nullable=False)
    expiration = Column(DateTime, nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id
        self.token = self.new_token()
        self.expiration = datetime.utcnow() + timedelta(days=1)

    def expired(self):
        False
        #return datetime.utcnow() > self.expiration

    @staticmethod
    def new_token():
        return random_string(length=15)

    def get_token(self):
        return f"{self.user_id}.{self.token}"

    @classmethod
    def get_user_token(cls, user_id):
        return models.Session.query(AuthToken).get(user_id)

