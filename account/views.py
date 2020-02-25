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

from django import http, shortcuts
from django.contrib.auth import decorators as auth_decorators
from django.views.decorators import http as http_decorators
from django.utils.decorators import method_decorator
from rest_framework import serializers, response, status

from django.contrib.auth import views as auth_views
from rest_framework import views as rest_views

from schoolmate import settings
from . import models


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def account(request):
    """Profile page
    """
    return shortcuts.render(request, 'account.html.j2')


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def logout(request):
    """Redirect to login after logout
    """
    return auth_views.logout_then_login(request)


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def password_change_done(request):
    """:return: 200 OK on successful password change
    """
    return http.HttpResponse(request, status=status.HTTP_200_OK)


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def user(request):
    """:return: JSON object with username
    """
    return http.JsonResponse({'username': request.user.username})


class UserInfoSerializer(serializers.ModelSerializer):
    school_form = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.SchoolUser
        fields = ('username', 'first_name', 'last_name', 'patronymic_name',
                  'birth_date', 'email', 'school_form', 'language')


@method_decorator(auth_decorators.login_required, name='dispatch')
class UserInfo(rest_views.APIView):
    """User info interface
    """
    model = models.SchoolUser

    def get(self, request):
        """:return: user info and available system languages
        """
        user_obj = self.model.objects.get(username=request.user.username)
        serializer = UserInfoSerializer(user_obj)
        user_info = serializer.data
        user_info.update({
            'languages': [
                {
                    'language_code': lang[0],
                    'language_name': lang[1]
                } for lang in settings.LANGUAGES
            ]
        })
        return response.Response(user_info, status=status.HTTP_200_OK)

    def patch(self, request):
        """Change user's language

        :return: 202 ACCEPTED; username and current locale
        :return: 400 BAD REQUEST; serializer's errors
        """
        user_obj = self.model.objects.get(username=request.user.username)
        serializer = UserInfoSerializer(
            user_obj, data={
                'username': request.user.username,
                'language': request.data.get('language', None)
            }
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.validated_data,
                                     status=status.HTTP_202_ACCEPTED)
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)
