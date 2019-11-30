import json
import models
from datetime import timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, or_, Float
from models import Base
from utils import random_string, utcnow
from models.deliveries import DeliveryStatus
from models.shops import Order


class BaseUser(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    creation_date = Column(DateTime, default=utcnow)
    status = Column(String, default="active")

    def valid_password(self, password):
        return self.password == password

    def change_password(self, new_password):
        self.password = new_password

    @property
    def is_active(self):
        return self.status == 'active'

    @classmethod
    def get_by_email(cls, email):
        return cls.query().filter(cls.email == email).scalar()


class FoodieUser(BaseUser):
    __tablename__ = 'foodie_user'

    phone = Column(String)
    role = Column(String)
    subscription = Column(String)
    photo_url = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    cash_balance = Column(Float, default=0)
    favor_balance = Column(Float, default=0)

    def is_premium(self):
        return self.subscription == 'premium'

    def is_user(self):
        return self.role == 'user'

    @property
    def is_delivery(self):
        return self.role == 'delivery'

    def available_for_delivery(self):
        location = DeliveryStatus.get_by_id(self.id)
        if not location or location.expired:
            return False
        else:
            return location.is_available

    def public_info(self):
        data = {
            'name': self.name,
            'surname': self.surname,
            'reputation': None,
        }
        return data

    def __repr__(self):  # pragma: no cover
        return f'Foodie User: id: {self.id}, name: {self.name}'


class BaseAuthToken(Base):
    __abstract__ = True

    token = Column(String, nullable=False)
    expiration = Column(DateTime, nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id
        self.token = self.new_token()
        self.expiration = utcnow() + timedelta(days=1)

    def expired(self):
        False
        # return datetime.utcnow() > self.expiration

    @staticmethod
    def new_token():
        return random_string(length=15)

    @classmethod
    def generate_new_token(cls, _id):
        """
        Generate a new token for a given user (first time)
        """
        new = cls(_id)
        models.Session.add(new)
        models.Session.commit()
        return new

    def public_token(self):
        return f"{self.user_id}.{self.token}"

    @classmethod
    def get_user_token(cls, _id):
        current = cls.query().get(_id)
        if not current:
            return cls.generate_new_token(_id)
        else:
            return current

    @classmethod
    def validate_token(cls, public_token):
        try:
            user_id, token = public_token.split('.')
            user_id = int(user_id)
        except Exception:
            return None

        current = cls.query().get(user_id)
        if not current:
            return None
        else:
            return user_id if current.token == token else None

    def _as_dict(self):
        return {'token': self.public_token()}


class AuthToken(BaseAuthToken):
        __tablename__ = 'auth_token'

        user_id = Column(Integer, ForeignKey('foodie_user.id'), primary_key=True)


class PasswordRecoveryToken(Base):
    __tablename__ = 'password_recovery_token'

    user_id = Column(Integer, ForeignKey('foodie_user.id'), primary_key=True)
    token = Column(String, nullable=False)
    creation_date = Column(DateTime, default=utcnow)
    expiration = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

    def __init__(self, user_id):
        self.user_id = user_id
        self.token = self.new_token()
        self.creation_date = utcnow()
        self.expiration = self.creation_date + timedelta(days=1)
        self.used = False

    @property
    def expired(self):
        return utcnow() > self.expiration

    @property
    def valid(self):
        return (not self.expired and not self.used)

    @staticmethod
    def new_token():
        return random_string(length=15)

    @staticmethod
    def _generate_new_token(user_id):
        """
        Generate a new token for a given user (first time). NOT intended for 'public' use
        """
        new = PasswordRecoveryToken(user_id)
        new.save_to_db()
        return new

    def public_token(self):
        return f"{self.user_id}.{self.token}"

    def refresh(self):
        self.token = self.new_token()
        self.expiration = utcnow() + timedelta(days=1)
        self.used = False
        self.save_to_db()

    @classmethod
    def get_user_token(cls, user_id):
        return cls.query().get(user_id)

    @classmethod
    def generate_token(cls, user_id):
        current = cls.get_user_token(user_id)
        if not current:
            return cls._generate_new_token(user_id)
        elif not current.valid:
            current.refresh()
            return current
        else:
            return current

    @classmethod
    def validate_user_token(cls, user_id, token):
        current = cls.query().get(user_id)
        if current and current.token == token and current.valid:
            return True
        else:
            return False

    def __repr__(self):  # pragma: no cover
        return f'Token for user {self.user_id}, expiration: {self.expiration}, used: {self.used}'
