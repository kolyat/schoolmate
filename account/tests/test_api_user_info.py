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
from rest_framework import test, status
import pytest

from testutils import settings
from . import data_test_api_user_info


class TestUserInfoApi(test.APITestCase):
    """Test user info API"""

    def setUp(self):
        super().setUp()
        self.client.login(username=settings.USER_STUDENT['username'],
                          password=settings.USER_STUDENT['password'])

    def tearDown(self):
        super().tearDown()
        self.client.logout()

    def test_get_user_info(self):
        """Get user info
        """
        logging.info('Request: {}'.format(settings.USER_INFO_PATH))
        try:
            response = self.client.get(settings.USER_INFO_PATH)
            logging.info('Response code: {}'.format(response.status_code))
            logging.info('Response data: {}'.format(json.dumps(response.data)))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIsNotNone(
                data_test_api_user_info.validate_user_info(response.data)
            )
        except Exception as e:
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    pytest.main()
