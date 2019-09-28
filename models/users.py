import json
import models
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, desc
from sqlalchemy.types import TypeDecorator, VARCHAR
from models import Base
from utils import random_string, utcnow


class JSONEncodedValue(TypeDecorator):  # pragma: no cover
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
    creation_date = Column(DateTime, default=utcnow)
    photo_url = Column(String, nullable=True)

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
            'photo_url': self.photo_url,
            'creation_date': self.creation_date.isoformat(),
        }

    def is_premium(self):
        return self.subscription == 'premium'

    def is_user(self):
        return self.role == 'user'

    def valid_password(self, password):
        return self.password == password

    def save_to_db(self):
        models.Session.add(self)
        models.Session.commit()

    def change_password(self, new_password):
        self.password = new_password

    @classmethod
    def get_by_email(cls, email):
        return models.Session.query(FoodieUser).filter(FoodieUser.email == email).scalar()

    def __repr__(self):  # pragma: no cover
        return f'Foodie User: id: {self.id}, name: {self.name}'


class AuthToken(Base):
    __tablename__ = 'auth_token'

    user_id = Column(Integer, ForeignKey('foodie_user.id'), primary_key=True)
    token = Column(String, nullable=False)
    expiration = Column(DateTime, nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id
        self.token = self.new_token()
        self.expiration = utcnow() + timedelta(days=1)

    def expired(self):
        False
        #return datetime.utcnow() > self.expiration

    @staticmethod
    def new_token():
        return random_string(length=15)

    @staticmethod
    def generate_new_token(user_id):
        """
        Generate a new token for a given user (first time)
        """
        new = AuthToken(user_id)
        models.Session.add(new)
        models.Session.commit()
        return new

    def public_token(self):
        return f"{self.user_id}.{self.token}"

    @classmethod
    def get_user_token(cls, user_id):
        current = models.Session.query(AuthToken).get(user_id)
        if not current:
            return cls.generate_new_token(user_id)
        else:
            return current

    @classmethod
    def validate_token(cls, public_token):
        try:
            user_id, token = public_token.split('.')
            user_id = int(user_id)
        except:
            return None

        current = models.Session.query(AuthToken).get(user_id)
        if not current:
            return None
        else:
            return user_id if current.token == token else None

    def _as_dict(self):
        return {'token': self.public_token()}


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
    def generate_new_token(user_id):
        """
        Generate a new token for a given user (first time)
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

    def save_to_db(self):
        models.Session.add(self)
        models.Session.commit()

    @classmethod
    def get_user_token(cls, user_id):
        return models.Session.query(cls).get(user_id)

    @classmethod
    def generate_token(cls, user_id):
        current = cls.get_user_token(user_id)
        if not current:
            return cls.generate_new_token(user_id)
        elif not current.valid:
            current.refresh()
            return current
        else:
            return current

    @classmethod
    def validate_user_token(cls, user_id, token):
        current = models.Session.query(PasswordRecoveryToken).get(user_id)
        if current and current.token == token and current.valid:
            return True
        else:
            return False

    def __repr__(self):  # pragma: no cover
        return f'Token for user {self.user_id}, expiration: {self.expiration}, used: {self.used}'