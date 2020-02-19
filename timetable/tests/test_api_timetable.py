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

import logging
import json
import ddt
from rest_framework import test
import pytest

from testutils import settings, ddtutils
from . import data_test_api_timetable


@ddt.ddt
class TestTimetableApi(test.APITestCase):
    """Test timetable API"""

    def setUp(self):
        super().setUp()
        self.client.login(username=settings.USER_STUDENT['username'],
                          password=settings.USER_STUDENT['password'])

    def tearDown(self):
        super().tearDown()
        self.client.logout()

    @ddt.data(*ddtutils.prepare(data_test_api_timetable.positive_cases))
    @ddt.unpack
    def test_positive_cases(self, url, code, validate):
        """positive cases with response data

        :param url: URL
        :param code: expected code
        :param validate: validation function for response data
        """
        logging.info('Request: {}'.format(url))
        try:
            response = self.client.get(url)
            logging.info('Response code: {}'.format(response.status_code))
            logging.info('Response data: {}'.format(json.dumps(response.data)))
            self.assertEqual(response.status_code, code)
            self.assertIsNotNone(validate(response.data))
        except Exception as e:
            logging.error(e)
            self.fail(e)

    @ddt.data(*ddtutils.prepare(data_test_api_timetable.empty_cases))
    @ddt.unpack
    def test_empty_cases(self, url, code, data):
        """Cases with empty response data

        :param url: URL
        :param code: expected code
        :param data: expected response data
        """
        logging.info('Request: {}'.format(url))
        try:
            response = self.client.get(url)
            response_data = json.dumps(response.data)
            logging.info('Response code: {}'.format(response.status_code))
            logging.info('Response data: {}'.format(response_data))
            self.assertEqual(response.status_code, code)
            self.assertJSONEqual(response_data, data)
        except Exception as e:
            logging.error(e)
            self.fail(e)

    @ddt.data(*ddtutils.prepare(data_test_api_timetable.error_cases))
    @ddt.unpack
    def test_error_cases(self, url, code):
        """Test behaviour with invalid url

        :param url: wrong URL
        :param code: expected error code
        """
        logging.info('Request: {}'.format(url))
        try:
            response = self.client.get(url)
            logging.info('Response code: {}'.format(response.status_code))
            self.assertEqual(response.status_code, code)
        except Exception as e:
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    pytest.main()
