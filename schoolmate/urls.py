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

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.views import generic, i18n
from rest_framework import schemas

from schoolmate import settings


urlpatterns = [
    path('', include('school.urls')),

    path('profile/', include('account.urls')),
    path('news/', include('news.urls')),
    path('timetable/', include('timetable.urls')),
    path('diary/', include('diary.urls')),
    path('notebook/', include('notebook.urls')),

    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),

    path('openapi', schemas.get_schema_view(
        title='Schoolmate',
        description='School management system API',
        version='2.0',
        urlconf='schoolmate.urls'
    ), name='openapi-schema'),
    path('redoc/', generic.TemplateView.as_view(
            template_name='redoc.html.j2',
            extra_context={'schema_url': 'openapi-schema'}
        ), name='redoc'),

    path('favicon.ico', generic.RedirectView.as_view(
        url='{}img/favicon.ico'.format(settings.STATIC_URL))),
]
urlpatterns += i18n_patterns(path(
    'jsi18n/', i18n.JavaScriptCatalog.as_view(domain='django'),
    name='javascript-catalog'
))
