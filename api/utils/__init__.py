from functools import wraps
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from facebook import GraphAPI, GraphAPIError
from .auth import requires_admin_auth


def validates_post_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from utils.logging import MyLogger
            try:
                json_data = request.get_json(force=True)
                MyLogger.debug("Se manda a %s, el JSON: %r", schema.__name__, json_data)
                post_data = schema().load(json_data)
            except ValidationError as e:
                MyLogger.warning("Validation Error en %s, error: %r", schema.__name__, e.messages)
                return e.messages, 400
            return func(*args, post_data=post_data, **kwargs)

        return wrapper
    return decorator


def facebook_get_email(access_token):  # pragma: no cover
    try:
        graph = GraphAPI(access_token=access_token)
        data = graph.request('/me?fields=email')
        return data.get('email')
    except GraphAPIError:
        return None


class AdminResource(Resource):
    decorators = [ requires_admin_auth ]
