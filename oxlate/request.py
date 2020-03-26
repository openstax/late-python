from .headers import Headers

from copy import deepcopy

class Request:
    def __init__(self, data):
        self._data = deepcopy(data)

    def get_uri(self):
        return self._data.get('uri')

    def set_uri(self, uri):
        self._data['uri'] = uri

    def get_headers(self):
        return Headers(self._data['headers'])

    # def get_cookie(self, name, default=None):
    #     return self._cookies.get(name, default);

    # def viewer_country(self):
    #     viewer_country_header = self._data.get('headers', {}) \
    #                                       .get('cloudfront-viewer-country', [{}])[0] \
    #                                       .get('value', None)
    #     return viewer_country_header

    # def to_dict(self):
    #     return deepcopy(self._data)

    # def raw_headers_copy(self):
    #     return deepcopy(self._data['headers'])

    # def raw_cookies_copy(self):
    #     return deepcopy(self._cookies)

    # def __parsedCookies(self):
    #     parsedCookie = {}
    #     if self._data['headers'].get('cookie', None):
    #         for cookie in self._data['headers']['cookie'][0]['value'].split(';'):
    #             if cookie:
    #                 parts = cookie.split('=')
    #                 parsedCookie[parts[0].strip()] = parts[1].strip()
    #     return parsedCookie
