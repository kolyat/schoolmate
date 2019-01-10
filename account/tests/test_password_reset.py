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

import logging
import re
from selenium.webdriver.common.by import By
from django.utils.translation import gettext_lazy as _
from django.conf import settings as django_settings
from django.core import mail
import pytest

from testutils import settings, webutils
from . import data_test_password_reset


class TestPasswordReset(webutils.SchoolmateClient):
    """Test password reset procedure"""
    FORGOT_PASSWORD_BUTTON = '//div[@view_id="forgot_password_btn"]/div/button'
    EMAIL_FIELD = '//div[@view_id="email"]/div/input'
    EMAIL_FIELD_MSG = '//div[@view_id="email"]/div[@role="alert"]'
    RESET_BUTTON = '//div[@view_id="reset_btn"]/div/button'
    EMAIL_SENT_FORM = '[view_id=password_reset_sent_form]'
    BACK_TO_LOGIN_BUTTON = '//div[@view_id="back_to_login_btn"]/div/button'
    RESET_CONFIRM_BUTTON = '//div[@view_id="confirm_btn"]/div/button'
    RESET_NEW_PASSWORD1_FIELD = '//div[@view_id="new_password1"]/div/input'
    RESET_NEW_PASSWORD1_FIELD_MSG = \
        '//div[@view_id="new_password1"]/div[@role="alert"]'
    RESET_NEW_PASSWORD2_FIELD = '//div[@view_id="new_password2"]/div/input'
    RESET_NEW_PASSWORD2_FIELD_MSG = \
        '//div[@view_id="new_password2"]/div[@role="alert"]'
    PASSWORD_RESET_COMPLETE_FORM = '[view_id=password_reset_complete_form]'

    @pytest.mark.usefixtures('mailoutbox')
    def test_password_reset_scenario(self):
        """Password reset scenario
        """
        self.open(settings.LOGIN_URL)
        self.wait_for_ready_state_complete()
        self.click(self.FORGOT_PASSWORD_BUTTON, by=By.XPATH)
        try:
            self.wait_for_element(self.RESET_BUTTON, by=By.XPATH)
            self.assertEqual(_('Password reset'), self.get_page_title())
            logging.info('Trying to send e-mail to {} ...'.format(
                data_test_password_reset.user['email']))
            self.send_keys(
                self.EMAIL_FIELD, data_test_password_reset.user['email'],
                by=By.XPATH
            )
            self.click(self.RESET_BUTTON, by=By.XPATH)
            self.wait_for_ready_state_complete()
            self.wait_for_element(self.EMAIL_SENT_FORM)
            self.assertEqual(_('Password reset sent'), self.get_page_title())
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
            self.click(self.BACK_TO_LOGIN_BUTTON, by=By.XPATH)
            self.wait_for_ready_state_complete()
            self.assertEqual(_('Sign in'), self.get_page_title())
            logging.info('Go to {}'.format(link))
            self.open(link)
            self.wait_for_ready_state_complete()
            self.assertEqual(_('Password reset confirmation'),
                             self.get_page_title())
            logging.info('Check empty fields validation...')
            self.click(self.RESET_CONFIRM_BUTTON, by=By.XPATH)
            msg = self.wait_for_element(self.RESET_NEW_PASSWORD1_FIELD_MSG,
                                        by=By.XPATH).text
            self.assertEqual(_('Field can not be empty'), msg)
            msg = self.wait_for_element(self.RESET_NEW_PASSWORD2_FIELD_MSG,
                                        by=By.XPATH).text
            self.assertEqual(_('Field can not be empty'), msg)
            logging.info('Done')
            new_password = 'new_password'
            logging.info('Check new password mismatch handling...')
            self.send_keys(self.RESET_NEW_PASSWORD1_FIELD, new_password,
                           by=By.XPATH)
            self.click(self.RESET_CONFIRM_BUTTON, by=By.XPATH)
            msg = self.wait_for_element(self.MESSAGE, by=By.XPATH).text
            self.assertEqual(_('Passwords are not the same'), msg)
            logging.info('Done')
            logging.info('Set up new password: {}'.format(new_password))
            self.send_keys(self.RESET_NEW_PASSWORD2_FIELD, new_password,
                           by=By.XPATH)
            self.click(self.RESET_CONFIRM_BUTTON, by=By.XPATH)
            self.wait_for_ready_state_complete()
            self.wait_for_element(self.PASSWORD_RESET_COMPLETE_FORM)
            self.assertEqual(_('Password reset complete'),
                             self.get_page_title())
            logging.info('Done')
            logging.info('Back to login page')
            self.click(self.BACK_TO_LOGIN_BUTTON, by=By.XPATH)
            self.wait_for_ready_state_complete()
            self.assertEqual(_('Sign in'), self.get_page_title())
            logging.info('Trying old password: {}'.format(
                data_test_password_reset.user['password']))
            self.login(data_test_password_reset.user['username'],
                       data_test_password_reset.user['password'], wait=False)
            msg = self.wait_for_element(self.MESSAGE, by=By.XPATH).text
            self.assertEqual(_('Wrong username/password'), msg)
            logging.info('Passed')
            logging.info('Trying to log in with new password: {}'
                         ''.format(new_password))
            self.login(data_test_password_reset.user['username'], new_password)
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
        self.click(self.FORGOT_PASSWORD_BUTTON, by=By.XPATH)
        try:
            self.wait_for_ready_state_complete()
            self.wait_for_element(self.RESET_BUTTON, by=By.XPATH)
            self.assertEqual(_('Password reset'), self.get_page_title())
            logging.info('Check empty e-mail field validation...')
            self.click(self.RESET_BUTTON, by=By.XPATH)
            msg = self.wait_for_element(self.EMAIL_FIELD_MSG, by=By.XPATH).text
            self.assertEqual(_('E-mail can not be empty'), msg)
            logging.info('Done')
            logging.info('Check with invalid e-mail address...')
            self.send_keys(self.EMAIL_FIELD, 'email', by=By.XPATH)
            self.click(self.RESET_BUTTON, by=By.XPATH)
            msg = self.wait_for_element(self.EMAIL_FIELD_MSG, by=By.XPATH).text
            self.assertEqual(_('Must be valid e-mail address'), msg)
            logging.info('Done')
            logging.info('E-mail validation passed')
        except Exception as e:
            logging.error('Error in e-mail validation')
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    pytest.main()
