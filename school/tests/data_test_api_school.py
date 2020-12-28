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

if sys.version_info < (3, 5):
    from testutils.webutils import compile
else:
    from fastjsonschema import compile

endpoints = {
    'status': [
        settings.STATUS_PATH, status.HTTP_200_OK,
        compile({
            '$schema': 'http://json-schema.org/draft-07/schema#',
            'type': 'object',
            'properties': {
                'date_description': {
                    'type': 'array',
                    'minItems': 0,
                    'uniqueItems': False,
                    'items': {
                        'type': 'object',
                        'properties': {
                            'period_type': {'type': 'string', 'minLength': 1},
                            'description': {'type': 'string', 'minLength': 0}
                        },
                        'additionalProperties': False,
                        'required': ['period_type', 'description']
                    }
                },
                'day': {'type': 'integer', 'minimum': 1, 'maximum': 31},
                'time_description': {
                    'type': 'array',
                    'minItems': 0,
                    'uniqueItems': False,
                    'items': {
                        'type': 'object',
                        'properties': {
                            'description': {'type': 'string', 'minLength': 0}
                        },
                        'additionalProperties': False,
                        'required': ['description']
                    }
                },
                'hour': {'type': 'integer', 'minimum': 0, 'maximum': 23},
                'month': {'type': 'integer', 'minimum': 1, 'maximum': 12},
                'second': {'type': 'integer', 'minimum': 0, 'maximum': 59},
                'minute': {'type': 'integer', 'minimum': 0, 'maximum': 59},
                'year': {'type': 'integer', 'minimum': 0, 'maximum': 9999},
            },
            'additionalProperties': False,
            'required': [
                'date_description',
                'day',
                'time_description',
                'hour',
                'month',
                'second',
                'minute',
                'year'
            ]
        })
    ],
    'school_forms': [
        settings.SCHOOL_FORMS_PATH, status.HTTP_200_OK,
        compile({
            '$schema': 'http://json-schema.org/draft-07/schema#',
            'type': 'array',
            'minItems': 0,
            'uniqueItems': True,
            'items': {
                'type': 'object',
                'properties': {
                    'number': {'type': 'integer', 'minimum': 0},
                    'letters': {
                        'type': 'array',
                        'minItems': 1,
                        'uniqueItems': True,
                        'items': {'type': 'string', 'minLength': 1},
                    }
                },
                'additionalProperties': False,
                'required': ['number', 'letters']
            }
        })
    ],
    'schedule_year': [
        settings.SCHEDULE_YEAR_PATH, status.HTTP_200_OK,
        compile({
            '$schema': 'http://json-schema.org/draft-07/schema#',
            'type': 'array',
            'minItems': 0,
            'uniqueItems': True,
            'items': {
                'type': 'object',
                'properties': {
                    'description': {'type': 'string', 'minLength': 1},
                    'start_date': {'type': 'string', 'format': 'date'},
                    'end_date': {'type': 'string', 'format': 'date'},
                },
                'additionalProperties': False,
                'required': ['description', 'start_date', 'end_date']
            }
        })
    ],
    'schedule_day': [
        settings.SCHEDULE_DAY_PATH, status.HTTP_200_OK,
        compile({
            '$schema': 'http://json-schema.org/draft-07/schema#',
            'type': 'array',
            'minItems': 0,
            'uniqueItems': True,
            'items': {
                'type': 'object',
                'properties': {
                    'description': {'type': 'string', 'minLength': 1},
                    'start_time': {'type': 'string',
                                   'pattern': '\d{2}:\d{2}:\d{2}'},
                    'end_time': {'type': 'string',
                                 'pattern': '\d{2}:\d{2}:\d{2}'},
                },
                'additionalProperties': False,
                'required': ['description', 'start_time', 'end_time']
            }
        })
    ],
    'school_subjects': [
        settings.SCHOOL_SUBJECTS_PATH, status.HTTP_200_OK,
        compile({
            '$schema': 'http://json-schema.org/draft-07/schema#',
            'type': 'array',
            'minItems': 0,
            'uniqueItems': True,
            'items': {
                'type': 'object',
                'properties': {
                    'subject': {'type': 'string', 'minLength': 0},
                },
                'additionalProperties': False,
                'required': ['subject']
            }
        })
    ]
}
