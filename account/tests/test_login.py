# Schoolmate - school management system
# Copyright (C) 2018  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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
import ddt
from selenium.webdriver.common.by import By
from seleniumbase.config import settings as sbsettings
from django.utils.translation import gettext_lazy as _

from testutils import settings, ddtutils, webutils
from . import data_test_login


class TestLogin(webutils.SchoolmateClient):
    """Test normal login"""

    def test_admin_login(self):
        """Log in as administrator
        """
        logging.info('Log in as administrator')
        self.login(settings.ADMIN_USER, settings.ADMIN_PASS)
        time.sleep(sbsettings.SMALL_TIMEOUT)
        try:
            self.wait_for_ready_state_complete()
            self.assertEqual(_('Profile'), self.get_page_title())
            time.sleep(sbsettings.MINI_TIMEOUT)
            username = self.get_attribute(
                '//div[@view_id="username"]/div/input',
                'value',
                by=By.XPATH
            )
            self.assertEqual(settings.ADMIN_USER, username)
            logging.info('Login successful')
        except Exception as e:
            logging.error('Error while logging in as administrator')
            logging.error(e)
            self.fail(e)


@ddt.ddt
class TestLoginError(webutils.SchoolmateClient):
    """Test login errors"""

    @ddt.data(*ddtutils.prepare(data_test_login.validation_data))
    @ddt.unpack
    def test_login_validation(self, creds, selector, message):
        """Test form validation with {0}; expected - {2}

        :param creds: dict with form data
        :param selector: message's CSS selector
        :param message: text with validation message
        """
        logging.info('Trying {}'.format(creds))
        self.login(creds['username'], creds['password'])
        try:
            self.wait_for_text_visible(message, selector, by=By.XPATH)
            logging.info('Validation passed')
        except Exception as e:
            logging.error('Error in form validation: {}'.format(creds))
            logging.error(e)
            self.fail(e)

    @ddt.data(*ddtutils.prepare(data_test_login.wrong_creds))
    @ddt.unpack
    def test_login_error_message(self, creds):
        """Test login error message with {0}

        :param creds: dict with form data
        """
        logging.info('Trying {}'.format(creds))
        self.login(creds['username'], creds['password'])
        try:
            self.wait_for_text_visible(
                _('Wrong username/password'),
                '//div[@class="webix_message_area"]/div/div', by=By.XPATH
            )
            logging.info('Wrong credentials handling passed')
        except Exception as e:
            logging.error('Error in handling wrong credentials: {}'
                          ''.format(creds))
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    import pytest
    pytest.main()
