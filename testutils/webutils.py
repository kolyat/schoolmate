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

import seleniumbase
from selenium.webdriver.common.by import By

from . import settings


class SchoolmateClient(seleniumbase.BaseCase):
    MESSAGE = {'selector': '//div[@class="webix_message_area"]/div/div',
               'by': By.XPATH}

    LOGIN_USERNAME_FIELD = \
        {'selector': '//div[@view_id="username"]/div/input', 'by': By.XPATH}
    LOGIN_PASSWORD_FIELD = \
        {'selector': '//div[@view_id="password"]/div/input', 'by': By.XPATH}
    LOGIN_BUTTON = \
        {'selector': '//div[@view_id="login_btn"]/div/button', 'by': By.XPATH}

    USER_MENU = {'selector': '[webix_l_id="user_item"]', 'by': By.CSS_SELECTOR}
    LOGOUT_MENU_ITEM = \
        {'selector': '[webix_l_id="logout_item"]', 'by': By.CSS_SELECTOR}

    OLD_PASSWORD_FIELD = {
        'selector': '//div[@view_id="old_password"]/div/input',
        'by': By.XPATH
    }
    NEW_PASSWORD1_FIELD = {
        'selector': '//div[@view_id="new_password1"]/div/input',
        'by': By.XPATH
    }
    NEW_PASSWORD2_FIELD = {
        'selector': '//div[@view_id="new_password2"]/div/input',
        'by': By.XPATH
    }
    CHANGE_PASSWORD_BUTTON = {
        'selector': '//div[@view_id="change_password_btn"]/div/button',
        'by': By.XPATH
    }

    def login(self, user, passwd, wait=True):
        """Log in to system

        :param user: username
        :param passwd: password
        :param wait: wait for main page load (True by default)
        """
        self.open(settings.LOGIN_URL)
        self.send_keys(new_value=user, **self.LOGIN_USERNAME_FIELD)
        self.send_keys(new_value=passwd, **self.LOGIN_PASSWORD_FIELD)
        self.click(**self.LOGIN_BUTTON)
        if wait:
            self.wait_for_ready_state_complete()
            self.wait_for_element(**self.USER_MENU)

    def logout(self, by_url=True):
        """Log out

        :param by_url: logout via URL (True bu default)
        """
        if by_url:
            self.open(settings.LOGOUT_URL)
        else:
            self.hover_on_element(**self.USER_MENU)
            self.click(**self.USER_MENU)
            self.wait_for_element_visible(**self.LOGOUT_MENU_ITEM)
            self.click(**self.LOGOUT_MENU_ITEM)
        self.wait_for_ready_state_complete()
        self.wait_for_element_visible(**self.LOGIN_BUTTON)

    def change_password(self, old, new1, new2):
        """Change password

        :param old: old password
        :param new1: new password
        :param new2: repeat new password
        """
        self.open(settings.PROFILE_URL)
        self.send_keys(new_value=old, **self.OLD_PASSWORD_FIELD)
        self.send_keys(new_value=new1, **self.NEW_PASSWORD1_FIELD)
        self.send_keys(new_value=new2, **self.NEW_PASSWORD2_FIELD)
        self.click(**self.CHANGE_PASSWORD_BUTTON)
