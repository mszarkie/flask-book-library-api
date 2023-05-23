from flask import request
from werkzeug.exceptions import UnsupportedMediaType
from functools import wraps


def validate_json_content_type(func):
    @wraps(func)
    def wrapper(*args, **kwagrs):
        data = request.get_json(silent=True)
        if data is None:
            raise UnsupportedMediaType('Content type must be application/json')
        return func(*args, **kwagrs)
    return wrapper