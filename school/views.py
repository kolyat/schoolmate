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

from django.template.response import TemplateResponse
from django.contrib.auth import decorators as auth_decorators
from django.views.decorators import http as http_decorators
from django.utils.decorators import method_decorator
from django.utils import timezone

from rest_framework import generics, views, response, status

from . import models, serializers


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def index(request):
    """Main page
    """
    return TemplateResponse(request, 'index.html.j2', context={})


@method_decorator(auth_decorators.login_required, name='dispatch')
class Status(views.APIView):
    """Retrieve server's date and time with period descriptions.

    ```json
    {
        "date_description": [
            {
                "description": "2nd semester",
                "start_date": "2022-01-13",
                "end_date": "2022-05-25",
                "period_type": "Q"
            }
        ],
        "time_description": [
            {
                "description": "5th lesson",
                "start_time": "13:05:01",
                "end_time": "13:50:00"
            }
        ],
        "year": 2022,
        "month": 2,
        "day": 18,
        "hour": 13,
        "minute": 14,
        "second": 38
    }
    ```
    """

    def get(self, request):
        now = timezone.localtime(timezone.now())
        date = now.date()
        time = now.timetz()
        payload = {}
        ys_obj = models.YearSchedule.objects.filter(
            start_date__lte=date, end_date__gte=date
        ).order_by('-period_type')
        ys_serializer = serializers.YearSchedule(ys_obj, many=True)
        payload.update({'date_description': ys_serializer.data})
        for ys in ys_serializer.data:
            if ys.get('period_type', None) == 'Q':
                ds_obj = models.DailySchedule.objects.filter(
                        start_time__lte=time, end_time__gte=time
                )
                ds_serializer = serializers.DailySchedule(ds_obj, many=True)
                payload.update({'time_description': ds_serializer.data})
                break
        else:
            payload.update({'time_description': []})
        payload.update({
            'year': date.year, 'month': date.month, 'day': date.day,
            'hour': time.hour, 'minute': time.minute, 'second': time.second
        })
        return response.Response(payload, status=status.HTTP_200_OK)


@method_decorator(auth_decorators.login_required, name='dispatch')
class Forms(generics.ListAPIView):
    """Retrieve school forms.
    """
    serializer_class = serializers.Form
    queryset = models.FormNumber.objects.all()


@method_decorator(auth_decorators.login_required, name='dispatch')
class YearSchedule(generics.ListAPIView):
    """Retrieve schedule of current year.
    """
    serializer_class = serializers.YearSchedule

    def get_queryset(self):
        _date = timezone.localtime(timezone.now()).date()
        return models.YearSchedule.objects.filter(
            school_year__start_date__lte=_date,
            school_year__end_date__gte=_date
        ).order_by('start_date')


@method_decorator(auth_decorators.login_required, name='dispatch')
class DailySchedule(generics.ListAPIView):
    """Retrieve daily schedule.
    """
    serializer_class = serializers.DailySchedule
    queryset = models.DailySchedule.objects.all().order_by('start_time')


class Subjects(generics.ListAPIView):
    """Retrieve school subjects.
    """
    serializer_class = serializers.Subject
    queryset = models.SchoolSubject.objects.all().order_by('subject')
