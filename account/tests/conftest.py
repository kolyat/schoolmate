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

import pytest

from account import models
from testutils import settings
from . import data_test_password_change, data_test_password_reset


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture()
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        models.SchoolUser.objects.create_superuser(
            username=settings.ADMIN_USER,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASS
        )
        models.SchoolUser.objects.create_user(
            data_test_password_change.user['username'],
            data_test_password_change.user['email'],
            data_test_password_change.user['password']
        )
        models.SchoolUser.objects.create_user(
            data_test_password_reset.user['username'],
            data_test_password_reset.user['email'],
            data_test_password_reset.user['password']
        )
