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

import pytest

from school.management.commands.populate_db_school import prepare_school
from account.management.commands.populate_db_account import prepare_account
from timetable.management.commands.populate_db_timetable import prepare_timetable


# @pytest.fixture(autouse=True)
# def enable_db_access_for_all_tests(db):
#     pass


@pytest.fixture
def prepare_test_school(db):
    prepare_school()


@pytest.fixture
def prepare_test_accounts(db, prepare_test_school):
    prepare_account()


@pytest.fixture
def prepare_test_timetable(db):
    prepare_timetable(forms=[9, 10, 11])
