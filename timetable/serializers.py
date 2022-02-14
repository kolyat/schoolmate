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


class Lesson(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    classroom = serializers.SlugRelatedField(slug_field='room_id',
                                             read_only=True)

    class Meta:
        model = models.Timetable
        fields = ('day_of_week', 'lesson_number', 'subject', 'classroom')


class Timetable(serializers.ModelSerializer):
    lessons = Lesson(many=True)
    form_number = serializers.IntegerField(
        source='school_form.form_number.number')
    form_letter = serializers.CharField(
        source='school_form.form_letter.letter')

    class Meta:
        model = models.TimetableSchoolForm
        fields = ('form_number', 'form_letter', 'lessons')
