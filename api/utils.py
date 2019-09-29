from functools import wraps
from flask import request
from marshmallow import ValidationError
from facebook import GraphAPI, GraphAPIError


def validates_post_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                post_data = schema().load(request.get_json(force=True))
            except ValidationError as e:
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
