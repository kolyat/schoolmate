# Schoolmate - school management system
# Copyright (C) 2018-2021  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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

import prepare_db
from school.management.commands.populate_db_school import prepare_school
from account.management.commands.populate_db_account import prepare_account
from news.management.commands.populate_db_news import prepare_news
from timetable.management.commands.populate_db_timetable import prepare_timetable


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope='session', autouse=True)
def django_db_modify_db_settings():
    pass


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    from django.conf import settings
    db_name = settings.DATABASES['default']['NAME']
    settings.DATABASES['default']['NAME'] = 'test_' + db_name
    django_db_blocker.unblock()
    db = prepare_db.Db(settings.DATABASES['default'], settings.BASE_DIR)
    db.create()
    for a in prepare_db.APPS:
        db.remove_migrations(a)
    for a in prepare_db.APPS:
        db.make_migrations(a)
    db.migrate()
    # for a in prepare_db.APPS:
    #     db.populate(a)
    prepare_school()
    prepare_account()
    prepare_news(number_of_articles=9)
    prepare_timetable(forms=[9, 11])
