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

from django import http
from django.template.response import TemplateResponse
from django.contrib.auth import decorators as auth_decorators
from django.contrib.auth import views as auth_views
from django.views.decorators import http as http_decorators
from django.utils.decorators import method_decorator
from rest_framework import response, status, generics

from schoolmate import settings
from . import models, serializers


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def account(request):
    """Profile page
    """
    return TemplateResponse(request, 'account.html.j2', context={})


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def logout(request):
    """Redirect to login after logout.
    """
    return auth_views.logout_then_login(request)


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def password_change_done(request):
    """200 OK on successful password change.
    """
    return http.HttpResponse(request, status=status.HTTP_200_OK)


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def user(request):
    """Retrieve username of current user.

    ```json
    {
        "username": "sam"
    }
    ```
    """
    return http.JsonResponse({'username': request.user.username})


@method_decorator(auth_decorators.login_required, name='dispatch')
class UserInfo(generics.RetrieveAPIView):
    """Retrieve user's info and settings.
    """
    serializer_class = serializers.UserInfo

    def get_object(self):
        return models.SchoolUser.objects.get(username=self.request.user)


@method_decorator(auth_decorators.login_required, name='dispatch')
class UserSettings(generics.UpdateAPIView):
    """Change settings of current user.
    """
    serializer_class = serializers.UserSettings

    def get_object(self):
        return models.SchoolUser.objects.get(username=self.request.user)
