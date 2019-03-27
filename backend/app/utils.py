from datetime import datetime
from json import loads
from .exceptions import ValidationError


class AttributeDict(dict):

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


def check_json(json, required):
    for item in required:
        if item not in json:
            raise ValidationError(f'{item} es necesario.')


def json_load(json, convert_date=True):
    json = loads(json) if isinstance(json, str) else json
    return AttributeDict(json)
