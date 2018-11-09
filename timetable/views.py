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

from django import shortcuts
from django.contrib.auth import decorators as auth_decorators
from django.views.decorators import http as http_decorators
from django.utils.decorators import method_decorator
from rest_framework import views, serializers, response, status

from . import models


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def timetable(request):
    """Timetable page
    """
    return shortcuts.render(request, 'timetable.html.j2')
