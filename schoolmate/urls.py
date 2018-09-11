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

from django.contrib import admin
from django.urls import include, path
from django.views import generic, i18n

from schoolmate import settings


urlpatterns = [
    path('', include('account.urls')),
    path('admin/', admin.site.urls),
    path('jsi18n/', i18n.JavaScriptCatalog.as_view(),
         name='javascript-catalog'),
    path('favicon.ico', generic.RedirectView.as_view(
        url='{}img/favicon.ico'.format(settings.STATIC_URL))),
]
