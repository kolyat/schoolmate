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

import time
import logging
from django.utils.translation import gettext_lazy as _
import pytest

from testutils import settings, webutils


class TestLogout(webutils.SchoolmateClient):
    """Test logout procedure
    """
    def test_logout(self):
        """Normal logout
        """
        logging.info('Normal logout procedure test')
        self.login(settings.USER_STUDENT['username'],
                   settings.USER_STUDENT['password'])
        time.sleep(3)
        try:
            self.logout(by_url=False)
            self.assertEqual(_('Sign in'), self.get_page_title())
            logging.info('Logout successful')
        except Exception as e:
            logging.error('Error during logout')
            logging.error(e)
            self.fail(e)

    def test_logout_without_login(self):
        """Logout without login
        """
        logging.info('Logout without login test')
        self.open(settings.BASE_URL)
        try:
            self.wait_for_ready_state_complete()
            self.assertEqual(_('Sign in'), self.get_page_title())
            self.logout()
            self.wait_for_ready_state_complete()
            self.assertEqual(_('Sign in'), self.get_page_title())
            logging.info('Logout without login passed')
        except Exception as e:
            logging.error('Logout without login failed')
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    pytest.main()
