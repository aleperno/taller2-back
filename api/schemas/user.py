from marshmallow import (
    fields,
    Schema,
    validate,
    validates_schema,
    ValidationError
    )
from api.validators import email_not_existing, password_validate


class NewUserSchema(Schema):
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True, validate=email_not_existing)
    password = fields.Str(validate=password_validate, required=True)
    phone = fields.Str(required=True)
    role = fields.Str(missing='user', validate=validate.OneOf(choices=['user', 'delivery']))
    subscription = fields.Str(missing='flat', validate=validate.OneOf(choices=['flat', 'premium']))
    photo_url = fields.Url(required=False)

    @validates_schema
    def validate_photo(self, data, **kwargs):
        if data['role'] == 'delivery' and not data.get('photo_url'):
            raise ValidationError("Delivery must upload photo", field_name='photo_url')
