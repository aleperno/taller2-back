from marshmallow import (
    fields,
    Schema,
    validates_schema,
    ValidationError,
    )
from api.validators import shop_exists


class NewShopSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    address = fields.Str(required=True)
    location = fields.Str(required=True)
    category = fields.Str(required=True)


class NewProductSchema(Schema):
    shop_id = fields.Int(required=True, validate=shop_exists)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    category = fields.Str(required=True)
    price = fields.Float(required=True)

