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
# along with this program. If not, see <http://www.gnu.org/licenses

from django.template.response import TemplateResponse

from schoolmate import settings
from .. import models


class SkinMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if type(response) == TemplateResponse:
            user = getattr(request, 'user', None)
            if not user:
                response.context_data['skin'] = settings.DEFAULT_SKIN
            elif not user.is_authenticated:
                response.context_data['skin'] = settings.DEFAULT_SKIN
            else:
                skin = models.SchoolUser.objects.get(username=user).skin
                response.context_data['skin'] = skin
        return response
