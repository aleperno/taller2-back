from marshmallow import (
    fields,
    Schema,
    )


class NewUserSchema(Schema):
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
