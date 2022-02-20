# Schoolmate - school management system
# Copyright (C) 2018-2022  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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

from django.contrib.auth import decorators as auth_decorators
from django.utils.decorators import method_decorator
from rest_framework import generics

from schoolmate import settings
from . import models, serializers


@method_decorator(auth_decorators.login_required, name='dispatch')
class Article(generics.ListAPIView):
    """Retrieve list of news (latest 300 articles by default).

    Number of articles is set in `LATEST_NEWS_COUNT` in project's `settings.py`.
    """
    serializer_class = serializers.Article
    queryset = models.Article.objects.all()[:settings.LATEST_NEWS_COUNT]
