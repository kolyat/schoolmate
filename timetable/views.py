# Schoolmate - school management system
# Copyright (C) 2018-2023  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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

from django.template.response import TemplateResponse
from django.contrib.auth import decorators as auth_decorators
from django.views import View
from django.utils.decorators import method_decorator
from django.utils import timezone
from rest_framework import generics

from . import models, serializers


@method_decorator(auth_decorators.login_required, name='dispatch')
class Timetable(View):
    default_context = {'form_number': 0}

    def get(self, request):
        try:
            _context = {'form_number': request.GET['form_number']}
        except Exception:
            _context = self.default_context
        return TemplateResponse(request, 'timetable.html.j2', context=_context)


@method_decorator(auth_decorators.login_required, name='dispatch')
class TimetableData(generics.ListAPIView):
    """Retrieve timetable.

    *Required URL parameter*: `form_number=[integer]` (0 – get whole timetable
    for all school forms).
    """
    serializer_class = serializers.Timetable

    def get_queryset(self):
        _date = timezone.localtime(timezone.now()).date()
        params = {'year__school_year__start_date__lte': _date,
                  'year__school_year__end_date__gte': _date}
        try:
            _form_number = self.request.query_params['form_number']
            _form_number = int(_form_number)
        except Exception:
            _form_number = None
        if _form_number is None:
            queryset = models.TimetableSchoolForm.objects.none()
        elif _form_number > 0:
            params.update({'school_form__form_number__number': _form_number})
            queryset = models.TimetableSchoolForm.objects.filter(**params)
        elif _form_number == 0:
            queryset = models.TimetableSchoolForm.objects.filter(**params)
        else:
            queryset = models.TimetableSchoolForm.objects.none()
        return queryset
