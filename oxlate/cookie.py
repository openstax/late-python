import re
import datetime

class Cookie:
    def __init__(self, name, value=None, expires_at=None, expires_days_from_now=None, path=None, domain=None):
        if expires_at and expires_days_from_now:
            raise ValueError("Do not specify both `expires_at` and `expires_days_from_now`")
        elif expires_days_from_now:
            self._expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=expires_days_from_now)
        else:
            self._expires_at = expires_at

        self._name = name
        self._value = value
        self._path = path
        self._domain = domain

    def value(self):
        components = ['{}={}'.format(self._name, self._value or "")]

        if self._expires_at:
            expires_str = self._expires_at.strftime("%a, %d %b %Y %H:%M:%S GMT")
            components.append('Expires={}'.format(expires_str))

        if self._path:
            components.append("Path={}".format(self._path))

        if self._domain:
            components.append("Domain={}".format(self._domain))

        return "; ".join(components)
