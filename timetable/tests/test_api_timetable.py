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
import ddt
from rest_framework import test

from testutils import settings, ddtutils
from . import data_test_api_timetable


@ddt.ddt
class TestTimetableApi(test.APITestCase):
    """Test timetable API"""

    def setUp(self):
        self.client.login(username=settings.USER_STUDENT['username'],
                          password=settings.USER_STUDENT['password'])

    def tearDown(self):
        self.client.logout()

    @ddt.data(*ddtutils.prepare(data_test_api_timetable.error_cases))
    @ddt.unpack
    def test_login_validation(self, url, code):
        """Test behaviour with invalid url

        :param url: wrong URL
        :param code: expected error code
        """
        response = self.client.get(url)
        self.assertEqual(response.status_code, code)


if __name__ == '__main__':
    import pytest
    pytest.main()
