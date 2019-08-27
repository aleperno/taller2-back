from marshmallow import (
    fields,
    Schema,
    )


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)