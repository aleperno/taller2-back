from marshmallow import (
    fields,
    Schema,
    validates_schema,
    ValidationError,
    )


class NewShopSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    address = fields.Str(required=True)
    location = fields.Str(required=True)
    category = fields.Str(required=True)