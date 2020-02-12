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

from rest_framework import status

from testutils.settings import TIMETABLE_DATA_PATH as p


positive_cases = {
    '9': [p + '9', status.HTTP_200_OK, None],
    '0': [p + '0', status.HTTP_200_OK, None],
}
empty_cases = {
    '999': [p + '999', status.HTTP_200_OK, []],
    'empty': [p, status.HTTP_200_OK, []],
    'qp_minus1': [p + '?form_number=-1', status.HTTP_200_OK, []],
    'qp_abc': [p + '?form_number=abc', status.HTTP_200_OK, []],
    'qp_empty': [p + '?form_number=', status.HTTP_200_OK, []]
}
error_cases = {
    'minus1': [p + '-1', status.HTTP_404_NOT_FOUND],
    'xyz': [p + 'xyz', status.HTTP_404_NOT_FOUND],
}
