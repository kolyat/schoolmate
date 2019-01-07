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
import re
from selenium.webdriver.common.by import By
from seleniumbase.config import settings as sbsettings
from django.utils.translation import gettext_lazy as _
from django.conf import settings as django_settings
from django.core import mail
import pytest

from testutils import settings, webutils
from . import data_test_password_reset


class TestPasswordReset(webutils.SchoolmateClient):
    """Test password reset procedure"""

    @pytest.mark.usefixtures('mailoutbox')
    def test_password_reset_scenario(self):
        """Password reset scenario
        """
        self.open(settings.LOGIN_URL)
        self.wait_for_ready_state_complete()
        self.click('//div[@view_id="forgot_password_btn"]/div/button',
                   by=By.XPATH)
        time.sleep(sbsettings.SMALL_TIMEOUT / 2)
        try:
            self.wait_for_ready_state_complete()
            self.assertEqual('Password reset', self.get_page_title())
            logging.info('Trying to send e-mail to {} ...'.format(
                data_test_password_reset.user['email']))
            self.send_keys(
                '//div[@view_id="email"]/div/input',
                data_test_password_reset.user['email'],
                by=By.XPATH
            )
            self.click('//div[@view_id="reset_btn"]/div/button', by=By.XPATH)
            time.sleep(sbsettings.MINI_TIMEOUT)
            self.wait_for_ready_state_complete()
            self.assertEqual('Password reset sent', self.get_page_title())
            logging.info('Passed')
            logging.info('Mail count in dummy outbox: {}'.format(
                len(mail.outbox)))
            self.assertEqual(1, len(mail.outbox))
            logging.info('From: {}'.format(mail.outbox[0].from_email))
            self.assertEqual(django_settings.DEFAULT_FROM_EMAIL,
                             mail.outbox[0].from_email)
            logging.info('To: {}'.format(mail.outbox[0].to[0]))
            self.assertEqual(data_test_password_reset.user['email'],
                             mail.outbox[0].to[0])
            logging.info('Subject: {}'.format(mail.outbox[0].subject))
            self.assertEqual('Schoolmate - password reset confirmation',
                             mail.outbox[0].subject)
            logging.info('Body: {}'.format(mail.outbox[0].body))
            email_to = re.search('(?P<email>\S+@\S+\.\S+)',
                                 mail.outbox[0].body).group('email')
            self.assertEqual(data_test_password_reset.user['email'],
                             email_to)
            link = re.search(
                '(?P<link>http.?://\S+/password_reset/\S+/\S+/)',
                mail.outbox[0].body
            ).group('link')
            logging.info('Back to login page')
            self.click('//div[@view_id="back_to_login_btn"]/div/button',
                       by=By.XPATH)
            time.sleep(sbsettings.MINI_TIMEOUT / 2)
            self.wait_for_ready_state_complete()
            self.assertEqual('Sign in', self.get_page_title())
            logging.info('Go to {}'.format(link))
            self.open(link)
            time.sleep(sbsettings.MINI_TIMEOUT / 2)
            self.wait_for_ready_state_complete()
            self.assertEqual('Password reset confirmation',
                             self.get_page_title())
            logging.info('Check empty fields validation...')
            self.click('//div[@view_id="confirm_btn"]/div/button', by=By.XPATH)
            self.wait_for_text_visible(
                _('Field can not be empty'),
                '//div[@view_id="new_password1"]/div[@role="alert"]',
                by=By.XPATH
            )
            self.wait_for_text_visible(
                _('Field can not be empty'),
                '//div[@view_id="new_password2"]/div[@role="alert"]',
                by=By.XPATH
            )
            logging.info('Done')
            new_password = 'new_password'
            logging.info('Check new password mismatch handling...')
            self.send_keys('//div[@view_id="new_password1"]/div/input',
                           new_password, by=By.XPATH)
            self.click('//div[@view_id="confirm_btn"]/div/button', by=By.XPATH)
            self.wait_for_text_visible(
                _('Passwords are not the same'),
                '//div[@class="webix_message_area"]/div/div', by=By.XPATH
            )
            logging.info('Done')
            logging.info('Set up new password: {}'.format(new_password))
            self.send_keys('//div[@view_id="new_password2"]/div/input',
                           new_password, by=By.XPATH)
            self.click('//div[@view_id="confirm_btn"]/div/button', by=By.XPATH)
            time.sleep(sbsettings.MINI_TIMEOUT / 2)
            self.wait_for_ready_state_complete()
            self.assertEqual('Password reset complete',
                             self.get_page_title())
            logging.info('Done')
            logging.info('Back to login page')
            self.click('//div[@view_id="back_to_login_btn"]/div/button',
                       by=By.XPATH)
            time.sleep(sbsettings.MINI_TIMEOUT / 2)
            self.wait_for_ready_state_complete()
            self.assertEqual('Sign in', self.get_page_title())
            logging.info('Trying old password: {}'.format(
                data_test_password_reset.user['password']))
            self.login(data_test_password_reset.user['username'],
                       data_test_password_reset.user['password'])
            self.wait_for_text_visible(
                _('Wrong username/password'),
                '//div[@class="webix_message_area"]/div/div', by=By.XPATH
            )
            logging.info('Passed')
            logging.info('Trying to log in with new password: {}'
                         ''.format(new_password))
            self.login(data_test_password_reset.user['username'], new_password)
            time.sleep(sbsettings.SMALL_TIMEOUT)
            self.wait_for_ready_state_complete()
            self.assertEqual(_('Profile'), self.get_page_title())
            logging.info('Password reset procedure test passed')
        except Exception as e:
            logging.error('Error during password reset procedure')
            logging.error(e)
            self.fail(e)

    def test_email_validation_for_password_reset(self):
        """Test e-mail validation for password reset
        """
        self.open(settings.LOGIN_URL)
        self.wait_for_ready_state_complete()
        self.click('//div[@view_id="forgot_password_btn"]/div/button',
                   by=By.XPATH)
        time.sleep(sbsettings.SMALL_TIMEOUT / 2)
        try:
            self.wait_for_ready_state_complete()
            self.assertEqual('Password reset', self.get_page_title())
            logging.info('Check empty e-mail field validation...')
            self.click('//div[@view_id="reset_btn"]/div/button', by=By.XPATH)
            self.wait_for_text_visible(
                _('E-mail can not be empty'),
                '//div[@view_id="email"]/div[@role="alert"]', by=By.XPATH
            )
            logging.info('Done')
            logging.info('Check with invalid e-mail address...')
            self.send_keys('//div[@view_id="email"]/div/input', 'email',
                           by=By.XPATH)
            self.click('//div[@view_id="reset_btn"]/div/button', by=By.XPATH)
            self.wait_for_text_visible(
                _('Must be valid e-mail address'),
                '//div[@view_id="email"]/div[@role="alert"]', by=By.XPATH
            )
            logging.info('Done')
            logging.info('E-mail validation passed')
        except Exception as e:
            logging.error('Error in e-mail validation')
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    pytest.main()
