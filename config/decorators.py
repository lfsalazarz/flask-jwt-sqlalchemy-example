# Standard library imports
from functools import wraps
from json import loads
# pydantic imports
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
