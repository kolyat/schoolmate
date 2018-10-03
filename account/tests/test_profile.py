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
from selenium.webdriver.common.by import By
from seleniumbase.config import settings as sbsettings

from testutils import rndutils, webutils
from account import models


class TestProfile(webutils.SchoolmateClient):
    """Test profile info"""

    def test_user_info(self):
        """Check data in user info form
        """
        user_info = rndutils.new_schooluser()
        username = user_info.pop('username')
        email = user_info.pop('email')
        password = user_info.pop('password')
        models.SchoolUser.objects.create_user(username, email, password,
                                              **user_info)
        logging.info('Log in as {}'.format(username))
        self.login(username, password)
        time.sleep(sbsettings.SMALL_TIMEOUT)
        try:
            self.wait_for_ready_state_complete()
            time.sleep(sbsettings.MINI_TIMEOUT / 2)
            self.assertEqual(username, self.get_attribute(
                '//div[@view_id="username"]/div/input', 'value', by=By.XPATH
            ))

            self.assertEqual(user_info['first_name'], self.get_attribute(
                '//div[@view_id="first_name"]/div/input', 'value', by=By.XPATH
            ))
            self.assertEqual(user_info['last_name'], self.get_attribute(
                '//div[@view_id="last_name"]/div/input', 'value', by=By.XPATH
            ))
            self.assertEqual(user_info['patronymic_name'], self.get_attribute(
                '//div[@view_id="patronymic_name"]/div/input', 'value',
                by=By.XPATH
            ))
            self.assertEqual(user_info['birth_date'], self.get_attribute(
                '//div[@view_id="birth_date"]/div/input', 'value', by=By.XPATH
            ))
            self.assertEqual(email, self.get_attribute(
                '//div[@view_id="email"]/div/input', 'value', by=By.XPATH
            ))
            self.assertEqual(user_info['school_form'], self.get_attribute(
                '//div[@view_id="school_form"]/div/input', 'value', by=By.XPATH
            ))
            logging.info('Profile check successful')
        except Exception as e:
            logging.error('Profile check error')
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    import pytest
    pytest.main()
