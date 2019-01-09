# Schoolmate - school management system
# Copyright (C) 2018-2019  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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

from rest_framework import generics, views, serializers, response, status

from . import models


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def index(request):
    """Main page
    """
    return shortcuts.render(request, 'index.html.j2')


class DailyScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailySchedule
        fields = ('description',)


class YearScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.YearSchedule
        fields = ('period_type', 'description')


class Status(views.APIView):
    @method_decorator(auth_decorators.login_required)
    def get(self, request):
        """:return: server's date and time with period description
        """
        now = timezone.localtime(timezone.now())
        date = now.date()
        time = now.timetz()
        status_info = dict()
        ys_obj = models.YearSchedule.objects.filter(
            start_date__lte=date, end_date__gte=date).order_by('-period_type')
        ys_serializer = YearScheduleSerializer(ys_obj, many=True)
        status_info.update({'date_description': ys_serializer.data})
        for ys in ys_serializer.data:
            if ys['period_type'] == 'Q':
                ds_obj = models.DailySchedule.objects.filter(
                        start_time__lte=time, end_time__gte=time)
                ds_serializer = DailyScheduleSerializer(ds_obj, many=True)
                status_info.update({'time_description': ds_serializer.data})
                break
        else:
            status_info.update({'time_description': list()})
        status_info.update({
            'year': date.year, 'month': date.month, 'day': date.day,
            'hour': time.hour, 'minute': time.minute, 'second': time.second
        })
        return response.Response(status_info, status=status.HTTP_200_OK)


class FormNumberSerializer(serializers.ModelSerializer):
    letters = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.FormNumber
        fields = ('number', 'letters')


@method_decorator(auth_decorators.login_required, name='dispatch')
class Forms(generics.ListAPIView):
    serializer_class = FormNumberSerializer
    queryset = models.FormNumber.objects.all()


class YearScheduleViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.YearSchedule
        fields = ('description', 'start_date', 'end_date')


@method_decorator(auth_decorators.login_required, name='dispatch')
class YearScheduleView(generics.ListAPIView):
    serializer_class = YearScheduleViewSerializer

    def get_queryset(self):
        _date = timezone.localtime(timezone.now()).date()
        return models.YearSchedule.objects.filter(
            school_year__start_date__lte=_date,
            school_year__end_date__gte=_date
        ).order_by('start_date')


class DailyScheduleViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailySchedule
        fields = ('description', 'start_time', 'end_time')


@method_decorator(auth_decorators.login_required, name='dispatch')
class DailyScheduleView(generics.ListAPIView):
    serializer_class = DailyScheduleViewSerializer
    queryset = models.DailySchedule.objects.all().order_by('start_time')
