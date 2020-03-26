import json
import re

from .headers import Headers
from .cookie import Cookie

class Response:
    def __init__(self, status=200, content_type='text/plain', body=None):
        self.set_status(status)
        self.set_content_type(content_type)
        self.set_body(body)
        self._cookies = []
        self._headers = Headers()

    def set_status(self, value):
        self._status = value
        return self

    def set_content_type(self, content_type):
        self._content_type = content_type
        return self

    def set_content_type_json(self):
        self._content_type = "application/json"
        return self

    def set_content_type_html(self):
        self._content_type = "text/html"
        return self

    def set_body(self, body):
        self._body = body
        return self

    def add_cookie(self, name, value=None, expires_at=None, path=None, domain=None):
        self._cookies.append(Cookie(name=name, value=value, expires_at=expires_at, path=path, domain=domain))
        return self

    def delete_cookie(self, name, path=None, domain=None):
        self._cookies.append(Cookie(name=name, value="", expires_days_from_now=-1000, path=path, domain=domain))

    def set_header(self, name, value):
        self._headers.set(name=name, value=value)
        return self

    def to_dict(self):
        result = {
            'status': self._status
        }

        if self._body is not None:
            result['body'] = self.__encoded_body()
            self._headers.set(name='Content-Type', value=self._content_type)

        for cookie in self._cookies:
            self._headers.set(name='Set-Cookie', value=cookie.value(), adjust_case_to_allow_duplicates=True)

        result['headers'] = self._headers.to_dict()

        return result

    def __encoded_body(self):
        if re.search(r'json', self._content_type):
            return json.dumps(self._body)
        else:
            return self._body
