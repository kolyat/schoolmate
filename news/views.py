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

from django.contrib.auth import decorators as auth_decorators
from django.utils.decorators import method_decorator
from rest_framework import serializers, views, response, status

from . import models


class ArticleSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = models.Article
        fields = ('created', 'header', 'content', 'author')


class ArticleView(views.APIView):
    @method_decorator(auth_decorators.login_required)
    def get(self, request):
        """:return: certain number of articles from defined position
        """
        count = request.data.get('count', 10)
        start = request.data.get('start', 0)
        queryset = models.Article.objects.all()[start:start+count]
        serializer = ArticleSerializer(queryset, many=True)
        total_records = models.Article.objects.all().count()
        data = {'data': serializer.data, 'pos': start,
                'total_count': total_records}
        return response.Response(data, status=status.HTTP_200_OK)
