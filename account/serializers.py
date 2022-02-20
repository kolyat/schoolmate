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

from rest_framework import serializers

from schoolmate import settings
from . import models


class UserInfo(serializers.ModelSerializer):
    school_form = serializers.StringRelatedField(many=False)
    languages = serializers.SerializerMethodField()
    skins = serializers.SerializerMethodField()

    class Meta:
        model = models.SchoolUser
        fields = (
            'username', 'first_name', 'last_name', 'patronymic_name',
            'birth_date', 'email', 'school_form',
            'language', 'languages', 'skin', 'skins'
        )

    def get_languages(self, obj):
        return [
            {
                'language_code': language[0],
                'language_name': language[1]
            } for language in settings.LANGUAGES
        ]

    def get_skins(self, obj):
        return [
            {
                'skin': skin[0],
                'skin_name': skin[1]
            } for skin in settings.SKINS
        ]


class UserSettings(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.SchoolUser
        fields = ('user', 'language', 'skin')
