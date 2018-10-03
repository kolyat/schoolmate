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

from django.utils.translation import gettext_lazy as _

from testutils import rndutils


user = rndutils.new_schooluser()

validation_data = {
    'empty_old_password': [
        {'old_password': '',
         'new_password1': 'new_password', 'new_password2': 'new_password'},
        '//div[@view_id="old_password"]/div[@role="alert"]',
        _('Field can not be empty')
    ],
    'empty_new_password1': [
        {'old_password': user['password'],
         'new_password1': '', 'new_password2': 'new_password'},
        '//div[@view_id="new_password1"]/div[@role="alert"]',
        _('Field can not be empty')
    ],
    'empty_new_password2': [
        {'old_password': user['password'],
         'new_password1': 'new_password', 'new_password2': ''},
        '//div[@view_id="new_password2"]/div[@role="alert"]',
        _('Field can not be empty')
    ]
}
