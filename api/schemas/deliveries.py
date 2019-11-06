from marshmallow import (
    fields,
    Schema,
    validate,
    validates_schema,
    ValidationError
    )
from api.validators import user_id_exists


class DeliveryStatusSchema(Schema):
    user_id = fields.Int(required=True, validate=user_id_exists)
    location = fields.String(required=True)
    available = fields.Boolean(required=False)