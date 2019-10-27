from flask import request
from functools import wraps
from api.schemas.auth import RequiresAuthorization
from marshmallow import ValidationError, EXCLUDE
from models.users import AuthToken
from models.admins import AdminAuthToken


def requires_token(token_cls, id_key):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                auth = RequiresAuthorization(unknown=EXCLUDE).load(dict(request.headers))
            except ValidationError as e:
                return e.messages, 403
            token = auth.get('Authorization')
            _id = token_cls.validate_token(token)
            if _id:
                kwargs.update({id_key: _id})
                kw = {id_key: _id}
                return func(*args, **kw)
            else:
                return "Bad Token", 403
        return wrapper
    return decorator


requires_user_auth = requires_token(AuthToken, 'user_id')
requires_admin_auth = requires_token(AdminAuthToken, 'admin_id')
