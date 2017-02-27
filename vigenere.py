import string

CHARS = list(string.printable)


def index(li, idx):
    return li[idx % len(li)]


def encode(text, key):
    repeated_code = []
    for x in range(len(text)):
        repeated_code.append(index(key, x))
    repeated_code = ''.join(repeated_code)

    result = []
    for x, y in zip(text, repeated_code):
        result.append(index(CHARS, CHARS.index(x) + CHARS.index(y)))
    return ''.join(result)


def decode(code, key):
    repeated_code = []
    for x in range(len(code)):
        repeated_code.append(index(key, x))
    repeated_code = ''.join(repeated_code)

    result = []
    for x, y in zip(code, repeated_code):
        result.append(index(CHARS, CHARS.index(x) - CHARS.index(y)))
    return ''.join(result)
