NUMERALS = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
}

EVERYTHING = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    **NUMERALS,
}


def find_calibration_values(haystack, candidates):
    i_first = len(haystack)
    i_last = -1

    d_first = ""
    d_last = ""

    for needle, digit in candidates.items():
        try:
            index = haystack.index(needle)
            if index < i_first:
                i_first = index
                d_first = digit
        except ValueError:
            pass

        try:
            index = haystack.rindex(needle)
            if index > i_last:
                i_last = index
                d_last = digit
        except ValueError:
            pass

    return int(d_first + d_last)


def run(data):
    total_numerals = 0
    total_everything = 0

    for line in data.splitlines():
        total_numerals += find_calibration_values(line, NUMERALS)
        total_everything += find_calibration_values(line, EVERYTHING)

    return total_numerals, total_everything
