from models import Base
from datetime import timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from utils import utcnow
from models.users import BaseAuthToken, BaseUser


class FoodieAdmin(BaseUser):
    __tablename__ = 'foodie_admin'


class AdminAuthToken(BaseAuthToken):
    __tablename__ = 'admin_auth_token'

    admin_id = Column(Integer, ForeignKey('foodie_admin.id'), primary_key=True)

    def __init__(self, admin_id):
        self.admin_id = admin_id
        self.token = self.new_token()
        self.expiration = utcnow() + timedelta(days=1)

    @property
    def user_id(self):
        return self.admin_id
