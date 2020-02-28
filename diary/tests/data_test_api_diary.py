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


validate = fastjsonschema.compile({
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'definitions': {
        'record': {
            'type': 'object',
            'properties': {
                'date': {'type': 'string', 'format': 'date'},
                'id': {'type': 'integer'},
                'lesson_number': {'type': 'integer', 'minimum': 1, 'maximum': 7},
                'subject': {'type': 'string'},
                'text': {'type': 'string'},
                'marks': {'type': 'string'},
                'signature': {'type': 'string'},
            },
            'additionalProperties': False,
            'required': ['date', 'lesson_number', 'subject', 'text']
        }
    },
    'oneOf': [
        {
            'type': 'array',
            'minItems': 6,
            'maxItems': 6,
            'items': {'$ref': '#/definitions/record'}
        },
        {'$ref': '#/definitions/record'}
    ]
})
