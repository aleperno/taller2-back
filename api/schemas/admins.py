from marshmallow import (
    fields,
    Schema,
    validate,
    validates_schema,
    ValidationError
    )
from api.validators import admin_not_existing, password_validate, email_not_existing


class NewAdminSchema(Schema):
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True, validate=admin_not_existing)
    password = fields.Str(validate=password_validate, required=True)


class ChangePasswordSchema(Schema):
    password = fields.Str(validate=password_validate, required=True)


class EditUserSchema(Schema):
    name = fields.Str(required=False)
    surname = fields.Str(required=False)
    email = fields.Email(required=False)
    password = fields.Str(validate=password_validate, required=False)
    phone = fields.Str(required=False)
    role = fields.Str(validate=validate.OneOf(choices=['user', 'delivery']))
    subscription = fields.Str(validate=validate.OneOf(choices=['flat', 'premium']))
    photo_url = fields.Url(required=False)
    active = fields.Boolean(required=False)
    cash_balance = fields.Float(required=False)
    favor_balance = fields.Float(required=False)


class PricingSchema(Schema):
    flat_min_km = fields.Integer(required=True)
    flat_base = fields.Integer(required=True)
    flat_extra_km = fields.Integer(required=True)
    premium_min_km = fields.Integer(required=True)
    premium_base = fields.Integer(required=True)
    premium_extra_km = fields.Integer(required=True)
    delivery_revenue_perc = fields.Integer(required=True)