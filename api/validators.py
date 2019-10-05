from marshmallow import (ValidationError,
                         validate,
                         )
from models.users import FoodieUser
from models.shops import FoodieShop


password_validate = validate.Length(min=6)


def email_not_existing(email):
    exists = FoodieUser.get_by_email(email)
    if exists:
        raise ValidationError('Email already exists')


def email_exists(email):
    exists = FoodieUser.get_by_email(email)
    if not exists:
        raise ValidationError('Email not found')


def shop_exists(shop_id):
    if not FoodieShop.query().get(shop_id):
        raise ValidationError(f'Shop id {shop_id} doesnt exist')
