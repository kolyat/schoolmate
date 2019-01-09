# Schoolmate - school management system
# Copyright (C) 2018-2019  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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

from testutils import ddtutils, rndutils, webutils
from account import models
from . import data_test_password_change as data


class TestPasswordChange(webutils.SchoolmateClient):
    """Test normal password change"""

    def test_password_change_with_relogin(self):
        """Change password and re-login
        """
        user = rndutils.new_schooluser()
        models.SchoolUser.objects.create_user(user['username'], user['email'],
                                              user['password'])
        new_password = 'new_password'
        logging.info('Log in as {}:{}'.format(user['username'],
                                              user['password']))
        self.login(user['username'], user['password'])
        time.sleep(sbsettings.SMALL_TIMEOUT)
        try:
            self.wait_for_ready_state_complete()
            logging.info('Change password to: {}'.format(new_password))
            self.change_password(user['password'], new_password, new_password)
            time.sleep(sbsettings.SMALL_TIMEOUT / 2)
            self.wait_for_text_visible(
                _('Password changed'),
                '//div[@class="webix_message_area"]/div/div', by=By.XPATH
            )
            self.maximize_window()
            logging.info('Log out')
            self.logout()
            self.wait_for_ready_state_complete()
            logging.info('Trying old password: {}'.format(user['password']))
            self.login(user['username'], user['password'])
            self.wait_for_text_visible(
                _('Wrong username/password'),
                '//div[@class="webix_message_area"]/div/div', by=By.XPATH
            )
            logging.info('Passed')
            logging.info('Log in (with new password) as {}:{}'.format(
                user['username'], new_password))
            self.login(user['username'], new_password)
            time.sleep(sbsettings.SMALL_TIMEOUT / 2)
            self.wait_for_ready_state_complete()
            self.assertEqual(_('Profile'), self.get_page_title())
            logging.info('Password change successful')
        except Exception as e:
            logging.error('Error in password change test')
            logging.error(e)
            self.fail(e)


@ddt.ddt
class PasswordChangeError(webutils.SchoolmateClient):
    """Test password change errors"""

    def setUp(self):
        super().setUp()
        self.login(data.user['username'], data.user['password'])
        time.sleep(sbsettings.SMALL_TIMEOUT)
        self.wait_for_ready_state_complete()

    @ddt.data(*ddtutils.prepare(data.validation_data))
    @ddt.unpack
    def test_password_change_validation(self, passwords, selector, message):
        """Test form validation with {0}; expected - {2}

        :param passwords: dict with form data
        :param selector: message's CSS selector
        :param message: text with validation message
        """
        logging.info('Password change test with: {}'.format(passwords))
        try:
            self.change_password(passwords['old_password'],
                                 passwords['new_password1'],
                                 passwords['new_password2'])
            self.wait_for_text_visible(message, selector, by=By.XPATH)
            logging.info('Validation passed')
        except Exception as e:
            logging.error('Error in form validation')
            logging.error(e)
            self.fail(e)

    def test_password_change_new_passwords_not_same(self):
        """New passwords don't match each other
        """
        new_password1 = 'new_password1'
        new_password2 = 'new_password2'
        logging.info(
            'Password change test, new passwords are not same: {} != {}'
            ''.format(new_password1, new_password2)
        )
        try:
            self.change_password(data.user['password'],
                                 new_password1, new_password2)
            self.wait_for_text_visible(
                _('New passwords are not the same'),
                '//div[@class="webix_message_area"]/div/div', by=By.XPATH
            )
            logging.info('Test passed')
        except Exception as e:
            logging.error('Error in form exception handling')
            logging.error(e)
            self.fail(e)

    def test_password_change_wrong_old_password(self):
        """Old password is wrong
        """
        old_password = 'old_password'
        new_password = 'new_password'
        logging.info('Password change test with wrong old password: {}'
                     ''.format(old_password))
        try:
            self.change_password(old_password, new_password, new_password)
            self.wait_for_text_visible(
                _('Password change failed'),
                '//div[@class="webix_message_area"]/div/div', by=By.XPATH
            )
            logging.info('Test passed')
        except Exception as e:
            logging.error('Error in form exception handling')
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    import pytest
    pytest.main()
