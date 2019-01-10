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

import seleniumbase
from selenium.webdriver.common.by import By

from . import settings


class SchoolmateClient(seleniumbase.BaseCase):
    MESSAGE = '//div[@class="webix_message_area"]/div/div'

    LOGIN_USERNAME_FIELD = '//div[@view_id="username"]/div/input'
    LOGIN_PASSWORD_FIELD = '//div[@view_id="password"]/div/input'
    LOGIN_BUTTON = '//div[@view_id="login_btn"]/div/button'

    USER_MENU = '[webix_l_id=user_item]'
    LOGOUT_MENU_ITEM = '[webix_l_id=logout_item]'

    OLD_PASSWORD_FIELD = '//div[@view_id="old_password"]/div/input'
    NEW_PASSWORD1_FIELD = '//div[@view_id="new_password1"]/div/input'
    NEW_PASSWORD2_FIELD = '//div[@view_id="new_password2"]/div/input'
    CHANGE_PASSWORD_BUTTON = '//div[@view_id="change_password_btn"]/div/button'

    def login(self, user, passwd, wait=True):
        """Log in to system

        :param user: username
        :param passwd: password
        :param wait: wait for main page load (True by default)
        """
        self.open(settings.LOGIN_URL)
        self.send_keys(self.LOGIN_USERNAME_FIELD, user, by=By.XPATH)
        self.send_keys(self.LOGIN_PASSWORD_FIELD, passwd, by=By.XPATH)
        self.click(self.LOGIN_BUTTON, by=By.XPATH)
        if wait:
            self.wait_for_ready_state_complete()
            self.wait_for_element(self.USER_MENU)

    def logout(self, by_url=True):
        """Log out

        :param by_url: logout via URL (True bu default)
        """
        if by_url:
            self.open(settings.LOGOUT_URL)
        else:
            self.hover_on_element(self.USER_MENU)
            self.click(self.USER_MENU)
            self.wait_for_element_visible(self.LOGOUT_MENU_ITEM)
            self.click(self.LOGOUT_MENU_ITEM)
        self.wait_for_ready_state_complete()
        self.wait_for_element_visible(self.LOGIN_BUTTON, by=By.XPATH)

    def change_password(self, old, new1, new2):
        """Change password

        :param old: old password
        :param new1: new password
        :param new2: repeat new password
        """
        self.open(settings.PROFILE_URL)
        self.send_keys(self.OLD_PASSWORD_FIELD, old, by=By.XPATH)
        self.send_keys(self.NEW_PASSWORD1_FIELD, new1, by=By.XPATH)
        self.send_keys(self.NEW_PASSWORD2_FIELD, new2, by=By.XPATH)
        self.click(self.CHANGE_PASSWORD_BUTTON, by=By.XPATH)
