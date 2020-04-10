from .headers import Headers

from copy import deepcopy

class Request:
    def __init__(self, data):
        self._data = data

    def get_uri(self):
        return self._data.get('uri')

    def set_uri(self, uri):
        self._data['uri'] = uri

    def get_headers(self):
        return Headers(self._data['headers'])

    def to_dict(self):
        return deepcopy(self._data)
