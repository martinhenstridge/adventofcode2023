import re

WORDS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

FORWARD_DIGITS_ONLY_REGEX = r"(\d)"
REVERSE_DIGITS_ONLY_REGEX = r"(\d)"

PARTIAL_REGEX = "|".join(WORDS)
FORWARD_WITH_WORDS_REGEX = rf"(\d|{PARTIAL_REGEX})"
REVERSE_WITH_WORDS_REGEX = rf"(\d|{PARTIAL_REGEX[::-1]})"


def find_number(haystack, regex):
    match = re.search(regex, haystack)
    string = match[1]

    if string.isdigit():
        return string

    try:
        return WORDS[string]
    except KeyError:
        return WORDS[string[::-1]]


def find_calibration_values(haystack, forward_regex, reverse_regex):
    first = find_number(haystack, forward_regex)
    last = find_number(haystack[::-1], reverse_regex)
    return int(first + last)


def run(data):
    total_digits_only = 0
    total_with_words = 0

    for line in data.splitlines():
        total_digits_only += find_calibration_values(
            line,
            forward_regex=FORWARD_DIGITS_ONLY_REGEX,
            reverse_regex=REVERSE_DIGITS_ONLY_REGEX,
        )
        total_with_words += find_calibration_values(
            line,
            forward_regex=FORWARD_WITH_WORDS_REGEX,
            reverse_regex=REVERSE_WITH_WORDS_REGEX,
        )

    return total_digits_only, total_with_words
