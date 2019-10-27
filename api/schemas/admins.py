from marshmallow import (
    fields,
    Schema,
    )
from api.validators import admin_not_existing, password_validate


class NewAdminSchema(Schema):
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True, validate=admin_not_existing)
    password = fields.Str(validate=password_validate, required=True)


class ChangePasswordSchema(Schema):
    password = fields.Str(validate=password_validate, required=True)
