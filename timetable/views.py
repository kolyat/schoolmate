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

from django import shortcuts
from django.contrib.auth import decorators as auth_decorators
from django.views.decorators import http as http_decorators
from django.utils.decorators import method_decorator
from django.utils import timezone
from rest_framework import generics, serializers

from . import models


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def timetable(request):
    """Timetable page
    """
    return shortcuts.render(request, 'timetable.html.j2')


class TimetableSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    classroom = serializers.SlugRelatedField(slug_field='room_id',
                                             read_only=True)

    class Meta:
        model = models.Timetable
        fields = ('day_of_week', 'lesson_number', 'subject', 'classroom')


class TimetableSchoolFormSerializer(serializers.ModelSerializer):
    lessons = TimetableSerializer(many=True)
    form_number = serializers.IntegerField(
        source='school_form.form_number.number')
    form_letter = serializers.CharField(
        source='school_form.form_letter.letter')

    class Meta:
        model = models.TimetableSchoolForm
        fields = ('form_number', 'form_letter', 'lessons')


@method_decorator(auth_decorators.login_required, name='dispatch')
class TimetableData(generics.ListAPIView):
    """Retrieve timetable (full or for specified school form number)
    """
    serializer_class = TimetableSchoolFormSerializer

    def get_queryset(self):
        _date = timezone.localtime(timezone.now()).date()
        params = {'year__school_year__start_date__lte': _date,
                  'year__school_year__end_date__gte': _date}
        _form_number = self.kwargs.get('form_number', None)
        try:
            _form_number = int(_form_number)
        except ValueError:
            _form_number = None
        except TypeError:
            _form_number = None
        if _form_number == None:
            queryset = models.TimetableSchoolForm.objects.none()
        elif _form_number > 0:
            params.update({'school_form__form_number__number': _form_number})
            queryset = models.TimetableSchoolForm.objects.filter(**params)
        elif _form_number == 0:
            queryset = models.TimetableSchoolForm.objects.filter(**params)
        else:
            queryset = models.TimetableSchoolForm.objects.none()
        return queryset
