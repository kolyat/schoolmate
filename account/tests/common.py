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

import logging
import seleniumbase

from testutils import settings


class Auth(seleniumbase.BaseCase):
    """Class with common authentication functions"""

    def login(self, user, passwd):
        """Log in to system

        :param user: username
        :param passwd: password
        """
        logging.info('Login - {}:{}'.format(user, passwd))
        self.open(settings.LOGIN_URL)
        self.send_keys('#username', user)
        self.send_keys('#password', passwd)
        self.click('#login_btn')

    def logout(self):
        """Log out
        """
        logging.info('Logging out')
        self.click('#user_item')
        self.click('#logout_item')
