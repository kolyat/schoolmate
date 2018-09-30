# Copyright (c) 2017-2018 Kirill 'Kolyat' Kiselnikov
# This file is the part of testutils, released under modified MIT license

import random
import itertools
import mimesis
import mimesis.builtins
from mimesis import enums

from schoolmate import settings


FORM_NUMBERS = [str(n) for n in range(1, 12)]
FORM_LETTERS = 'АБВ'
FORMS = [''.join(f) for f in itertools.product(FORM_NUMBERS, FORM_LETTERS)]


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


def new_schooluser():
    """Generate data for fake school user

    :return: dict with person data
    """
    random.seed()
    _person = mimesis.Person(locale='ru')
    _person_ru = mimesis.builtins.RussiaSpecProvider()
    _date = mimesis.Datetime()
    _gender = random.choice((enums.Gender.MALE, enums.Gender.FEMALE))
    _username = _person.username('ld')
    return {
        'username': _username,
        'password': _username,
        'first_name': _person.name(_gender),
        'last_name': _person.surname(_gender),
        'patronymic_name': _person_ru.patronymic(_gender),
        'birth_date': _date.date(start=1990, end=2000, fmt='%Y-%m-%d'),
        'email': _person.email(),
        'school_form': random.choice(FORMS),
        'language': random.choice(settings.LANGUAGES)[0],
        'is_active': True,
        'is_staff': False,
        'is_superuser': False
    }
