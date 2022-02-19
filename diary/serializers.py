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

from django.utils.translation import gettext as _
from rest_framework import serializers

from account import models as account_models
from school import models as school_models
from timetable import models as tt_models
from . import models


class Timetable(serializers.ModelSerializer):
    lesson_num = serializers.IntegerField(source='lesson_number')
    subject = serializers.StringRelatedField()

    class Meta:
        model = tt_models.Timetable
        fields = ('lesson_num', 'subject')


class DiaryRecordRead(serializers.ModelSerializer):
    date = serializers.DateField()
    subject = serializers.StringRelatedField()

    class Meta:
        model = models.DiaryRecord
        fields = ('date', 'lesson_number', 'subject', 'text')


class DiaryRecordWrite(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=False, many=False,
        queryset=account_models.SchoolUser.objects.all()
    )
    date = serializers.DateField()
    lesson_number = serializers.IntegerField()
    subject = serializers.PrimaryKeyRelatedField(
        read_only=False, many=False,
        queryset=school_models.SchoolSubject.objects.all()
    )

    class Meta:
        model = models.DiaryRecord
        fields = ('user', 'date', 'lesson_number', 'subject', 'text')

    def validate_lesson_number(self, value):
        """Perform lesson_number validation

        :param value: lesson_number

        :raise ValidationError:
            - value is null
            - value is not integer
            - value is not in range from 1 to 7 inclusive

        :return: value
        """
        if value is None:
            raise serializers.ValidationError(
                detail=_('lesson_number must be specified'),
                code='null'
            )
        elif not isinstance(value, int):
            raise serializers.ValidationError(
                detail=_('lesson_number must be integer'),
                code='type'
            )
        elif (value < 1) or (value > 7):
            raise serializers.ValidationError(
                detail=_('lesson_number must be in range '
                         'from 1 to 7 inclusive'),
                code='range'
            )
        else:
            return value
