# Schoolmate - school management system
# Copyright (C) 2018-2020  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
from rest_framework import status

if sys.version_info < (3, 5):
    from testutils.webutils import compile
else:
    from fastjsonschema import compile

validate_user_info = compile({
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'username': {'type': 'string', 'minLength': 1},
        'first_name': {'type': 'string', 'minLength': 0},
        'last_name': {'type': 'string', 'minLength': 0},
        'patronymic_name': {'type': ['string', 'null']},
        'birth_date': {
            'anyOf': [
                {'type': 'string', 'format': 'date'},
                {'type': 'null'}
            ]
        },
        'email': {'type': 'string', 'format': 'idn-email'},
        'school_form': {
            'anyOf': [
                {'type': 'string', 'pattern': '\d+\D+'},
                {'type': 'null'}
            ]
        },
        'language': {'type': 'string', 'minLength': 2},
        'languages': {
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'object',
                'properties': {
                    'language_code': {'type': 'string', 'minLength': 2},
                    'language_name': {'type': 'string', 'minLength': 2},
                },
                'additionalProperties': False,
                'required': ['language_code', 'language_name']
            }
        }
    },
    'additionalProperties': False,
    'required': [
        'username',
        'first_name',
        'last_name',
        'patronymic_name',
        'birth_date',
        'email',
        'school_form',
        'language',
        'languages'
    ]
})

lang_cases = {
    'positive': [
        {'language': 'de'}, status.HTTP_202_ACCEPTED, {'language': 'de'}
    ],
    'wrong_language': [
        {'language': 'xxx'}, status.HTTP_400_BAD_REQUEST, {'code': 'invalid_choice'}
    ],
    'wrong_type': [
        {'language': 123}, status.HTTP_400_BAD_REQUEST, {'code': 'invalid_choice'}
    ],
    'empty_language': [
        {'language': ''}, status.HTTP_400_BAD_REQUEST, {'code': 'invalid_choice'}
    ],
    'empty_payload': [
        {}, status.HTTP_400_BAD_REQUEST, {'code': 'null'}
    ],
}
