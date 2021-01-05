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

from django.core.management import base
from utils import rnd

from news import models as news_models
from schoolmate import settings


default_number = settings.LATEST_NEWS_COUNT * 2


def prepare_news(number_of_articles=default_number):
    """Generate defined number of news articles

    :param number_of_articles: number of news articles
    """
    print('Create data for NEWS app:')
    print('    {:.<25}...'.format('{} articles'.format(number_of_articles)),
          end='', flush=True)
    for _ in range(number_of_articles):
        article = rnd.new_article()
        news_models.Article(title=article['title'],
                            content=article['content']).save()
    print('OK')


class Command(base.BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        prepare_news()
