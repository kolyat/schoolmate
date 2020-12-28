# Schoolmate - school management system
# Copyright (C) 2018-2021  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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

from testutils import settings
from testutils.rndutils import random_str

if sys.version_info < (3, 5):
    from testutils.webutils import compile
else:
    from fastjsonschema import compile

validate = compile({
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'definitions': {
        'record': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'user': {'type': 'string', 'minLength': 1},
                'date': {'type': 'string', 'format': 'date'},
                'lesson_number': {'type': 'integer',
                                  'minimum': 1, 'maximum': 7},
                'subject': {'type': 'string'},
                'text': {'type': 'string'},
                'marks': {'type': 'string'},
                'signature': {'type': 'string'},
            },
            'additionalProperties': False,
            'required': ['date', 'lesson_number', 'subject', 'text']
        }
    },
    'anyOf': [
        {
            'type': 'array',
            'minItems': 7,
            'maxItems': 7,
            'items': {'$ref': '#/definitions/record'}
        },
        {'$ref': '#/definitions/record'},
        {'properties': {'school_form': {'type': 'string'}}},
        {'properties': {'lesson_number': {'type': 'string'}}},
        {'properties': {'subject': {'type': 'string'}}},
    ]
})

credentials = {
    'school_form_assigned': [
        settings.USER_STUDENT['username'], settings.USER_STUDENT['password'],
        status.HTTP_200_OK
    ],
    'school_form_not_assigned': [
        settings.USER_ADMIN['username'], settings.USER_ADMIN['password'],
        status.HTTP_424_FAILED_DEPENDENCY
    ]
}

template = {
    'lesson_number': 3,
    'subject': 'Физика',
    'text': 'Some text here'
}

positive_cases = {
    'lesson_3': [{'lesson_number': 3}, status.HTTP_201_CREATED],
    'lesson_1': [{'lesson_number': 1}, status.HTTP_201_CREATED],
    'lesson_7': [{'lesson_number': 7}, status.HTTP_201_CREATED],
    'subject_algebra': [{'subject': 'Алгебра'}, status.HTTP_201_CREATED],
    'subject_blank': [{'subject': ' '}, status.HTTP_201_CREATED],
    'text_non_empty': [{'text': 'For testing'}, status.HTTP_201_CREATED],
    'text_unicode': [{'text': random_str(9000)}, status.HTTP_201_CREATED],
    'text_empty': [{'text': ''}, status.HTTP_201_CREATED],
    'no_text': [
        {'lesson_number': 3, 'subject': 'Физика'},
        status.HTTP_201_CREATED
    ]
}

negative_cases = {
    'lesson_negative': [{'lesson_number': -1}, status.HTTP_400_BAD_REQUEST],
    'lesson_0': [{'lesson_number': 0}, status.HTTP_400_BAD_REQUEST],
    'lesson_8': [{'lesson_number': 8}, status.HTTP_400_BAD_REQUEST],
    'lesson_100': [{'lesson_number': 100}, status.HTTP_400_BAD_REQUEST],
    'lesson_float': [{'lesson_number': 3.5}, status.HTTP_400_BAD_REQUEST],
    'lesson_text': [{'lesson_number': '3'}, status.HTTP_201_CREATED],
    'lesson_null': [{'lesson_number': None}, status.HTTP_400_BAD_REQUEST],
    'subject_text': [{'subject': 'text'}, status.HTTP_400_BAD_REQUEST],
    'subject_null': [{'subject': None}, status.HTTP_400_BAD_REQUEST],
    'subject_123': [{'subject': 123}, status.HTTP_400_BAD_REQUEST],
    'text_123': [{'text': 123}, status.HTTP_201_CREATED],
    'text_null': [{'text': None}, status.HTTP_201_CREATED]
}

incomplete_payload = {
    'no_lesson_number': [
        {'subject': 'Физика', 'text': 'Some text here'},
        status.HTTP_400_BAD_REQUEST
    ],
    'no_subject': [
        {'lesson_number': 3, 'text': 'Some text here'},
        status.HTTP_400_BAD_REQUEST
    ]
}
