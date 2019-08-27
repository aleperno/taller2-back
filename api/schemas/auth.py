from marshmallow import (
    fields,
    Schema,
    )
from api.validators import email_exists


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)