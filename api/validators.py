from marshmallow import (ValidationError,
                         validate,
                         )
from models.users import FoodieUser
from models.admins import FoodieAdmin
from models.shops import FoodieShop, Product, Order


password_validate = validate.Length(min=6)


def email_not_existing(email):
    exists = FoodieUser.get_by_email(email)
    if exists:
        raise ValidationError('Email already exists')


def admin_not_existing(email):
    exists = FoodieAdmin.get_by_email(email)
    if exists:
        raise ValidationError('Email already exists')


def email_exists(email):
    exists = FoodieUser.get_by_email(email)
    if not exists:
        raise ValidationError('Email not found')


def user_id_exists(user_id):
    if not FoodieUser.get_by_id(user_id):
        raise ValidationError(f'User {user_id} doesnt exist', field_name='user_id')


def order_exists(order_id):
    if not Order.get_by_id(order_id):
        raise ValidationError(f'Order {order_id} doesnt exist', field_name='order_id')


def shop_exists(shop_id):
    if not FoodieShop.query().get(shop_id):
        raise ValidationError(f'Shop id {shop_id} doesnt exist')


def product_exists(product_id):
    if not Product.get_by_id(product_id):
        raise ValidationError(f'Product id {product_id} doesnt exist')


def product_belongs_shop(product_id, shop_id):
    if not Product.product_belongs_shop(product_id, shop_id):
        raise ValidationError(f'Product id {product_id} does not belong to shop {shop_id}', field_name='products')
    return True
