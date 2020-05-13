# Standard library imports
from functools import wraps
from json import loads

from flask import abort, request
from pydantic import ValidationError

# HTTP Status Codes
from config.constants import BAD_REQUEST


def validation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return {"err": loads(e.json())}, BAD_REQUEST

    return wrapper


def max_content_length(max_length):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            content_length = request.content_length
            if content_length is not None and content_length > max_length:
                abort(413, "Payload Too Large")
            return func(*args, **kwargs)
        return wrapper
    return decorator
