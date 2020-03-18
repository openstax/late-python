from .utils import string_to_case_number, case_number_to_string

class Headers:
    def __init__(self):
        self._data = {}

    def add(self, name, value, adjust_case_to_allow_duplicates=False):
        # import ipdb; ipdb.set_trace()
        if adjust_case_to_allow_duplicates:
            if self._data.get(name):
                # Collision, need to change case
                same_names_case_insensitive = list(filter(lambda key: key.lower() == name.lower(), self._data.keys()))
                existing_names_case_binary_representations = set(map(string_to_case_number, same_names_case_insensitive))
                available_case_binary_representations = sorted(set(range(pow(2,len(name)))) - existing_names_case_binary_representations)

                if len(available_case_binary_representations) == 0:
                    raise RuntimeError("There are no more case variants for header name " + name)
                else:
                    new_name = case_number_to_string(name, available_case_binary_representations[0])
                    self._data[new_name] = value
            else:
                # No collision
                self._data[name] = value
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
