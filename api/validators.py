from marshmallow import (ValidationError,
                         validate,
                         )
from models.users import FoodieUser


password_validate = validate.Length(min=6)


def email_not_existing(email):
    exists = FoodieUser.get_by_email(email)
    if exists:
        raise ValidationError('Email already exists')


def email_exists(email):
    exists = FoodieUser.get_by_email(email)
    if not exists:
        raise ValidationError('Email not found')
