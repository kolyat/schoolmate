import random


def random_char():
    """Get random UTF-8 character

    :return: non-space printable unicode character
    """
    random.seed()
    while True:
        char = chr(random.randint(0, 0x10FFFF))
        if char.isprintable() and not char.isspace():
            return char


def random_str(length=9):
    """Get string with random UTF-8 characters

    :param length: string's length (default = 9)
    :return: str
    """
    return ''.join([random_char() for _ in range(length)])


def random_numstr(length=9):
    """Get string with digits

    :param length: string's length (default = 9)
    :return: str
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def random_id():
    """Generate id between 100000 and 999999 inclusive

    :return: id int
    """
    random.seed()
    return random.randint(100000, 999999)
