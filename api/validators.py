from marshmallow import (ValidationError)
from models.users import FoodieUser


def email_not_existing(email):
    exists = FoodieUser.get_by_email(email)
    if exists:
        raise ValidationError('Email already exists')


def email_exists(email):  # pragma: no cover
    exists = FoodieUser.get_by_email(email)
    if not exists:
        raise ValidationError('Email not found')
