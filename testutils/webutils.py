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
import seleniumbase
from selenium.webdriver.common.by import By
from seleniumbase.config import settings as sbsettings

from . import settings


class SchoolmateClient(seleniumbase.BaseCase):
    def login(self, user, passwd):
        """Log in to system

        :param user: username
        :param passwd: password
        """
        self.open(settings.LOGIN_URL)
        self.send_keys('//div[@view_id="username"]/div/input', user,
                       by=By.XPATH)
        self.send_keys('//div[@view_id="password"]/div/input', passwd,
                       by=By.XPATH)
        self.click('//div[@view_id="login_btn"]/div/button', by=By.XPATH)

    def logout(self):
        """Log out
        """
        self.wait_for_element_visible('[webix_l_id=user_item]')
        self.hover_on_element('[webix_l_id=user_item]')
        time.sleep(sbsettings.MINI_TIMEOUT / 2)
        self.wait_for_element_visible('[webix_l_id=logout_item]')
        self.click('[webix_l_id=logout_item]')
