import re

BLANK_CHARS_SEQUENCE = re.compile('\s+')


def normalize_spaces(string: str):
    return BLANK_CHARS_SEQUENCE.sub(' ', string)


def stringify_number(i: int):
    if i % 10 == 1 and i != 11:
        return f'{i}st'
    elif i % 10 == 2 and i != 12:
        return f'{i}nd'
    elif i % 10 == 3 and i != 13:
        return f'{i}rd'
    else:
        return f'{i}th'
