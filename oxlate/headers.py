import re
from copy import deepcopy

ALPHA_REGEX = re.compile('[^a-zA-Z]')

class RequestCookies:
    def __init__(self, data):
        self._data = data

    def set(self, name, value=''):
        if 'cookie' not in self._data:
            self._data['cookie'] = [{'key': 'Cookie', 'value': ''}]
        old_cookie_string = self._data['cookie'][0]['value']

        parsed_cookies = RequestCookies._parse_cookies(old_cookie_string)
        parsed_cookies[name] = value

        new_cookie_string = RequestCookies._cookie_string(parsed_cookies)
        self._data['cookie'][0]['value'] = new_cookie_string

        return self

    def get(self, name, default=None):
        cookie_string = self._data \
                            .get('cookie', [{}])[0] \
                            .get('value', '')
        parsed_cookies = RequestCookies._parse_cookies(cookie_string)
        return parsed_cookies.get(name, default)

    @staticmethod
    def _cookie_string(parsed_cookies):
        entries = map(
            lambda elem: '{}={}'.format(elem[0], elem[1]),
            parsed_cookies.items(),
        )
        return ';'.join(entries)

    @staticmethod
    def _parse_cookies(string):
        parsed_cookies = {}
        for cookie_string in string.split(';'):
            if cookie_string:
                parts = cookie_string.split('=')
                parsed_cookies[parts[0].strip()] = parts[1].strip()
        return parsed_cookies

class ResponseCookie:
    def __init__(self, string):
        self._string     = string
        self._name       = None
        self._value      = None
        self._expires_at = None
        self._path       = None
        self._domain     = None

        for chunk in self._string.split(';'):
            match = re.search(r'\AExpires=(.+)\Z', chunk.strip())
            if match:
                continue

            match = re.search(r'\A(.+)=(.*)\Z', chunk.strip())
            if match:
                self._name  = match.group(1)
                self._value = match.group(2) if len(match.group(2)) > 0 else None

    def name(self):
        return self._name

    def value(self):
        return self._value

class ResponseCookies:
    def __init__(self, data):
        self._data = data

    def get(self, name, default=None):
        for key,value in self._data.items():
            if key.lower() == 'set-cookie':
                response_cookie = ResponseCookie(value[0]['value'])
                if response_cookie.name() == name:
                    return response_cookie.value()
        return default


    def set(self, name, value):
        return self

class Headers:
    def __init__(self, data=None):
        self._data = {} if data is None else data

        self._duplicate_name_counts = {}
        for name in self._data.keys():
            if name.lower() not in self._duplicate_name_counts:
                self._duplicate_name_counts[name.lower()] = -1
            self._duplicate_name_counts[name.lower()] += 1

    def get(self, name, default=None):
        return self._data.get(name, default)

    def get_value(self, name, default=None):
        return self._data.get(name, [{}])[0].get('value', default)

    # See https://forums.aws.amazon.com/thread.jspa?messageID=701434 about the duplicate stuff
    def set(self, name, value, adjust_case_to_allow_duplicates=False):
        if adjust_case_to_allow_duplicates:
            duplicate_name_count = self._duplicate_name_counts[name.lower()] = \
                self._duplicate_name_counts.get(name.lower(), -1) + 1
            adjusted_name = self._toggle_case_based_on_number(name, duplicate_name_count)
        else:
            adjusted_name = name

        adjusted_value = [{
            'key':   adjusted_name,
            'value': value,
        }]

        self._data[adjusted_name] = adjusted_value
        return self

    def get_request_cookie(self, name, default=None):
        request_cookies = RequestCookies(self._data)
        return request_cookies.get(name, default)

    def set_request_cookie(self, name, value):
        request_cookies = RequestCookies(self._data)
        request_cookies.set(name, value)
        return self

    def get_response_cookie(self, name):
        response_cookies = ResponseCookies(self._data)
        return response_cookies.get(name, default=None)

    def set_response_cookie(self, name, value):
        response_cookies = ResponseCookies(self._data)
        response_cookies.set(name=name, value=value)
        return self

    def to_dict(self):
        return deepcopy(self._data)

    def _toggle_case_based_on_number(self, string, number):
        alpha_only_string = ALPHA_REGEX.sub('', string)

        if number >= pow(2,len(alpha_only_string)):
            raise RuntimeError("There are no more case variants for header name " + string)

        number_as_binary_string = ('{0:' + str(len(alpha_only_string)) + 'b}').format(number)

        result = []

        # Move through the 1's and 0's in the binary string, changing cases in the input
        # string for alpha characters only.
        char_idx = 0
        for bit in number_as_binary_string:
            while not string[char_idx].isalpha():
                # skip non alpha characters
                result.append(string[char_idx])
                char_idx += 1

            # switch this letter to be upper or lower based on binary representation
            result.append(string[char_idx].upper() if bit == "1" else string[char_idx].lower())
            char_idx += 1

        return ''.join(result)
