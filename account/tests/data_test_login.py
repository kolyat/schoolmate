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

from django.utils.translation import gettext_lazy as _

from testutils import settings, rndutils


validation_data = {
    'user-empty_pass-correct': [
        {'username': '', 'password': settings.ADMIN_PASS},
        '//div[@view_id="username"]/div[@role="alert"]',
        _('Username can not be empty')
    ],
    'user-correct_pass-empty': [
        {'username': settings.ADMIN_USER, 'password': ''},
        '//div[@view_id="password"]/div[@role="alert"]',
        _('Password can not be empty')
    ]
}

wrong_creds = {
    'user-wrong_pass-correct': [{'username': 'a',
                                 'password': settings.ADMIN_PASS}],
    'user-correct_pass-wrong': [{'username': settings.ADMIN_USER,
                                 'password': 'n'}],
    'user-wrong_pass-wrong': [{'username': 'a', 'password': 'a'}],
    'swapped_userpass': [{'username': settings.ADMIN_PASS,
                          'password': settings.ADMIN_USER}],
    'random_userpass': [{'username': rndutils.random_str(),
                         'password': rndutils.random_str()}]
}
