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
from news.management.commands.populate_db_news import prepare_news
from timetable.management.commands.populate_db_timetable import prepare_timetable
from diary.management.commands.populate_db_diary import prepare_diary


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        prepare_school()
        prepare_account()
        prepare_news()
        prepare_timetable()
        prepare_diary()
