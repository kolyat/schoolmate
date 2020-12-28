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
import ddt
from rest_framework import test
import pytest

from testutils import settings, ddtutils
from . import data_test_api_school


@pytest.mark.skipif(sys.version_info < (3, 5),
                    reason='Requires Python 3.5 or higher')
@ddt.ddt
class TestSchoolApi(test.APITestCase):
    """Test school API
    """
    def setUp(self):
        super().setUp()
        self.client.login(username=settings.USER_STUDENT['username'],
                          password=settings.USER_STUDENT['password'])

    def tearDown(self):
        super().tearDown()
        self.client.logout()

    @ddt.data(*ddtutils.prepare(data_test_api_school.endpoints))
    @ddt.unpack
    def test_endpoints(self, url, code, validate):
        """Positive cases with response data

        :param url: URL
        :param code: expected code
        :param validate: validation function for response data
        """
        logging.info('Request: GET {}'.format(url))
        try:
            response = self.client.get(url)
            logging.info('Response code: {}'.format(response.status_code))
            logging.info('Response data: {}'.format(json.dumps(response.data)))
            self.assertEqual(response.status_code, code)
            self.assertIsNotNone(validate(response.data))
        except Exception as e:
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    pytest.main()
