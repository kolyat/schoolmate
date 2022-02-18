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

from . import models


class Form(serializers.ModelSerializer):
    letters = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.FormNumber
        fields = ('number', 'letters')


class YearSchedule(serializers.ModelSerializer):
    class Meta:
        model = models.YearSchedule
        fields = ('description', 'start_date', 'end_date', 'period_type')


class DailySchedule(serializers.ModelSerializer):
    class Meta:
        model = models.DailySchedule
        fields = ('description', 'start_time', 'end_time')


class Subject(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolSubject
        fields = ('subject',)
