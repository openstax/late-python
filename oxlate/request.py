class Request:
    def __init__(self, data):
        self._data = data
        self._headers = data.get('headers', {})
        self._cookies = self.__parsedCookies()

    def get_uri(self):
        return self._data.get('uri')

    def set_uri(self, uri):
        self._data['uri'] = uri

    def get_cookie(self, name, default=None):
        return self._cookies.get(name, default);

    def viewer_country(self):
        viewer_country_header = self._headers.get('cloudfront-viewer-country')
        if viewer_country_header:
            return viewer_country_header[0]['value']
        else:
            return None

    def to_dict(self):
        return dict(self._data)

    def raw_headers(self):
        return dict(self._headers)

    def raw_cookies(self):
        return dict(self._cookies)

    def __parsedCookies(self):
        parsedCookie = {}
        if self._headers.get('cookie'):
            for cookie in self._headers['cookie'][0]['value'].split(';'):
                if cookie:
                    parts = cookie.split('=')
                    parsedCookie[parts[0].strip()] = parts[1].strip()
        return parsedCookie
