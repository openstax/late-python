import re

ALPHA_REGEX = re.compile('[^a-zA-Z]')

class Headers:
    def __init__(self):
        self._data = {}
        self._duplicate_name_counts = {}

    # See https://forums.aws.amazon.com/thread.jspa?messageID=701434 about the duplicate stuff
    def add(self, name, value, adjust_case_to_allow_duplicates=False):
        if adjust_case_to_allow_duplicates:
            duplicate_name_count = self._duplicate_name_counts[name.lower()] = \
                self._duplicate_name_counts.get(name.lower(), -1) + 1

            deduped_name = self._toggle_case_based_on_number(name, duplicate_name_count)
            self._data[deduped_name] = value
        else:
            self._data[name] = value

    def to_dict(self):
        result = {}

        for key in self._data:
            result[key] = [
                {
                    'key': key,
                    'value': self._data[key]
                }
            ]

        return result

    def _toggle_case_based_on_number(self, string, number):
        alpha_only_string = ALPHA_REGEX.sub('', string)

        if number >= pow(2,len(alpha_only_string)):
            raise RuntimeError("There are no more case variants for header name " + string)

        number_as_binary_string = ('{0:' + str(len(alpha_only_string)) + 'b}').format(number)

        string_cursor = 0
        result = []

        # Move through the 1's and 0's in the binary string, changing cases in the input
        # string for alpha characters only.
        for bit in number_as_binary_string:
            while not string[string_cursor].isalpha():
                # skip non alpha characters
                result.append(string[string_cursor])
                string_cursor = string_cursor + 1

            # switch this letter to be upper or lower based on binary representation
            result.append(string[string_cursor].upper() if bit == "1" else string[string_cursor].lower())
            string_cursor = string_cursor + 1

        return "".join(result)
