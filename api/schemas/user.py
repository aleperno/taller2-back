from marshmallow import (
    fields,
    Schema,
    validate,
    validates_schema,
    ValidationError
    )
from api.validators import email_not_existing


class NewUserSchema(Schema):
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True, validate=email_not_existing)
    password = fields.Str(validate=validate.Length(min=6), required=True)
    phone = fields.Str(required=True)
    role = fields.Str(missing='user', validate=validate.OneOf(choices=['user', 'delivery']))
    subscription = fields.Str(missing='flat', validate=validate.OneOf(choices=['flat', 'premium']))
