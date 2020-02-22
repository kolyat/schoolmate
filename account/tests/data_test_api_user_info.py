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

import fastjsonschema


validate_user_info = fastjsonschema.compile({
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'username': {'type': 'string', 'minLength': 1},
        'first_name': {'type': 'string', 'minLength': 0},
        'last_name': {'type': 'string', 'minLength': 0},
        'patronymic_name': {'type': ['string', 'null']},
        'birth_date': {
            'anyOf': [
                {'type': 'string', 'pattern': '\d{4}-\d{2}-\d{2}'},
                {'type': 'null'}
            ]
        },
        'email': {'type': 'string', 'pattern': '[a-zA-Z-_.]{2,}@[a-zA-Z-_]{2,}(\.[a-zA-Z]{2,})+'},
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
                    'language_code': {'$ref': '#/language'},
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
