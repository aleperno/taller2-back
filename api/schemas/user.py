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
    role = fields.Str(missing='user')
    subscription = fields.Str(missing='flat')

    @validates_schema
    def validate_role(self, data, **kw):
        if data['role'] not in ['user', 'delivery']:
            raise ValidationError(message={'role': ['Not a valid value']})

    @validates_schema
    def validate_subscription(self, data, **kw):
        if data['subscription'] not in ['flat', 'premium']:
            raise ValidationError(message={'subscription': ['Not a valid value']})
