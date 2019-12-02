from marshmallow import (
    fields,
    Schema,
    validates_schema,
    ValidationError,
    )
from api.validators import email_exists, password_validate


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    firebase_token = fields.Str(required=False)


class ForgottenPasswordSchema(Schema):
    email = fields.Email(required=True, validate=email_exists)


class ResetPasswordSchema(Schema):
    email = fields.Email(required=True, validate=email_exists)
    password = fields.Str(validate=password_validate, required=True)
    confirm_password = fields.Str(validate=password_validate, required=True)
    token = fields.Str(required=True)

    @validates_schema
    def validate_new_password(self, data, **kwargs):
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords don't match", field_name='confirm_password')


class RequiresAuthorization(Schema):
    class Meta:
        additional_properties = fields.Raw()

    Authorization = fields.Str(required=True)


class FacebookLoginSchema(Schema):
    fb_access_token = fields.Str(required=True)
    firebase_token = fields.Str(required=False)
