
def string_to_case_number(string):
    binary_representation = list(map(lambda char: 1 if char.isupper() else 0, string))
    return int("".join(str(x) for x in binary_representation), 2)

def case_number_to_string(string, case_number):
    binary_representation = ('{0:' + str(len(string)) + 'b}').format(case_number)
    return "".join(
                map(
                  lambda i_char: i_char[1].upper() if binary_representation[i_char[0]] == "1" else i_char[1].lower(),
                  enumerate(string)
                )
              )
