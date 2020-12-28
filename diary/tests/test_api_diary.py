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
import logging
import json
import copy
from rest_framework import test
import ddt
import pytest

from testutils import settings, ddtutils
from . import data_test_api_diary


@pytest.mark.skipif(sys.version_info < (3, 5),
                    reason='Requires Python 3.5 or higher')
@ddt.ddt
class TestDiaryApiRetrieve(test.APITestCase):
    """Test diary API - retrieve records
    """
    @ddt.data(*ddtutils.prepare(data_test_api_diary.credentials))
    @ddt.unpack
    def test_retrieve(self, username, password, code):
        """Cases with response data

        :param username: user's username
        :param password: user's password
        :param code: expected code
        """
        self.client.login(username=username, password=password)
        url = settings.DIARY_PATH + '2021/02/29/'
        logging.info('Request: GET {}'.format(url))
        try:
            response = self.client.get(url)
            data = json.loads(response.content)
            logging.info('Response code: {}'.format(response.status_code))
            logging.info('Response data: {}'.format(data))
            self.assertEqual(response.status_code, code)
            self.assertIsNotNone(data_test_api_diary.validate(data))
        except Exception as e:
            logging.error(e)
            self.client.logout()
            self.fail(e)


@pytest.mark.skipif(sys.version_info < (3, 5),
                    reason='Requires Python 3.5 or higher')
@ddt.ddt
class TestDiaryApiWrite(test.APITestCase):
    """Test timetable API - create/update records
    """
    def setUp(self):
        super().setUp()
        self.client.login(username=settings.USER_STUDENT['username'],
                          password=settings.USER_STUDENT['password'])

    def tearDown(self):
        super().tearDown()
        self.client.logout()

    @ddt.data(*ddtutils.prepare(data_test_api_diary.positive_cases))
    @ddt.unpack
    def test_positive_cases(self, payload, code):
        """Positive create/update cases

        :param payload: additional payload
        :param code: expected code
        """
        url = settings.DIARY_PATH + '2021/03/01/'
        data = copy.deepcopy(data_test_api_diary.template)
        data.update(payload)
        logging.info('Request: POST {}'.format(url))
        logging.info('Payload: {}'.format(data))
        try:
            response = self.client.post(url, data)
            response_data = json.loads(response.content)
            logging.info('Response code: {}'.format(response.status_code))
            logging.info('Response data: {}'.format(response_data))
            self.assertEqual(response.status_code, code)
            self.assertIsNotNone(data_test_api_diary.validate(response_data))
            self.assertTrue(
                set(payload.items()).issubset(set(response_data.items()))
            )
        except Exception as e:
            logging.error(e)
            self.fail(e)

    @ddt.data(*ddtutils.prepare(data_test_api_diary.negative_cases))
    @ddt.unpack
    def test_negative_cases(self, payload, code):
        """Negative create/update cases

        :param payload: additional payload
        :param code: expected code
        """
        url = settings.DIARY_PATH + '2021/03/02/'
        data = copy.deepcopy(data_test_api_diary.template)
        data.update(payload)
        logging.info('Request: POST {}'.format(url))
        logging.info('Payload: {}'.format(data))
        try:
            response = self.client.post(url, data)
            response_data = json.loads(response.content)
            logging.info('Response code: {}'.format(response.status_code))
            logging.info('Response data: {}'.format(response_data))
            self.assertEqual(response.status_code, code)
            self.assertIsNotNone(data_test_api_diary.validate(response_data))
        except Exception as e:
            logging.error(e)
            self.fail(e)

    @ddt.data(*ddtutils.prepare(data_test_api_diary.incomplete_payload))
    @ddt.unpack
    def test_incomplete_payload(self, payload, code):
        """Negative tests with incomplete payload

        :param payload: incomplete payload
        :param code: expected code
        """
        url = settings.DIARY_PATH + '2021/03/03/'
        logging.info('Request: POST {}'.format(url))
        logging.info('Payload: {}'.format(payload))
        try:
            response = self.client.post(url, payload)
            response_data = json.loads(response.content)
            logging.info('Response code: {}'.format(response.status_code))
            logging.info('Response data: {}'.format(response_data))
            self.assertEqual(response.status_code, code)
            self.assertIsNotNone(data_test_api_diary.validate(response_data))
        except Exception as e:
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    pytest.main()
