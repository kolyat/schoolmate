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

from django.core.management import base
from testutils import rndutils

from news import models as news_models
from schoolmate import settings


def prepare_news():
    print('Create data for NEWS app:')
    print('    {:.<25}...'.format('News articles'), end='', flush=True)
    for _ in range(settings.LATEST_NEWS_COUNT * 2):
        news_models.Article(**rndutils.new_article()).save()
    print('OK')


class Command(base.BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        prepare_news()
