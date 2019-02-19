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
from selenium.webdriver.common.by import By

from testutils import rndutils, webutils
from school import models as school_models
from account import models as account_models


class TestProfile(webutils.SchoolmateClient):
    """Test profile info
    """
    PROFILE_MENU_ITEM = {'selector': '[webix_l_id="profile_item"]',
                         'by': By.CSS_SELECTOR}
    PROFILE_USERNAME_FIELD = \
        {'selector': '//div[@view_id="username"]/div/input', 'by': By.XPATH}
    PROFILE_FIRST_NAME_FIELD = \
        {'selector': '//div[@view_id="first_name"]/div/input', 'by': By.XPATH}
    PROFILE_LAST_NAME_FIELD = \
        {'selector': '//div[@view_id="last_name"]/div/input', 'by': By.XPATH}
    PROFILE_PATRONYMIC_NAME_FIELD = {
        'selector': '//div[@view_id="patronymic_name"]/div/input',
        'by': By.XPATH
    }
    PROFILE_BIRTH_DATE_FIELD = \
        {'selector': '//div[@view_id="birth_date"]/div/input', 'by': By.XPATH}
    PROFILE_EMAIL_FIELD = \
        {'selector': '//div[@view_id="email"]/div/input', 'by': By.XPATH}
    PROFILE_SCHOOL_FORM_FIELD = \
        {'selector': '//div[@view_id="school_form"]/div/input', 'by': By.XPATH}

    def test_user_info(self):
        """Check data in user info form
        """
        user_info = rndutils.new_schooluser()
        school_form = rndutils.new_schoolform()
        username = user_info.pop('username')
        email = user_info.pop('email')
        password = user_info.pop('password')
        # Prepare database
        _letter = school_models.FormLetter(letter=school_form['form_letter'])
        _letter.save()
        _number = school_models.FormNumber(number=school_form['form_number'])
        _number.save()
        _sf = school_models.SchoolForm(form_number=_number,
                                       form_letter=_letter)
        _sf.save()
        account_models.SchoolUser.objects.create_user(
            username, email, password, school_form=_sf, **user_info)
        # Start scenario
        logging.info('Log in as {}'.format(username))
        self.login(username, password)
        time.sleep(3)
        try:
            self.hover_on_element(**self.USER_MENU)
            self.click(**self.USER_MENU)
            self.wait_for_element_visible(**self.PROFILE_MENU_ITEM)
            self.click(**self.PROFILE_MENU_ITEM)
            self.wait_for_element(**self.PROFILE_SCHOOL_FORM_FIELD)
            time.sleep(1)
            self.assertEqual(username, self.get_attribute(
                attribute='value', **self.PROFILE_USERNAME_FIELD))
            self.assertEqual(user_info['first_name'], self.get_attribute(
                attribute='value', **self.PROFILE_FIRST_NAME_FIELD))
            self.assertEqual(user_info['last_name'], self.get_attribute(
                attribute='value', **self.PROFILE_LAST_NAME_FIELD))
            self.assertEqual(user_info['patronymic_name'], self.get_attribute(
                attribute='value', **self.PROFILE_PATRONYMIC_NAME_FIELD))
            self.assertEqual(user_info['birth_date'], self.get_attribute(
                attribute='value', **self.PROFILE_BIRTH_DATE_FIELD))
            self.assertEqual(email, self.get_attribute(
                attribute='value', **self.PROFILE_EMAIL_FIELD))
            self.assertEqual(
                ''.join((str(school_form['form_number']),
                         school_form['form_letter'])),
                self.get_attribute(attribute='value',
                                   **self.PROFILE_SCHOOL_FORM_FIELD)
            )
            logging.info('Profile check successful')
        except Exception as e:
            logging.error('Profile check error')
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    import pytest
    pytest.main()
