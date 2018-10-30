# Schoolmate - school management system
# Copyright (C) 2018  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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

from django.contrib.auth import decorators as auth_decorators
from django.utils.decorators import method_decorator
from django.utils import timezone

from rest_framework import serializers, response, status
from rest_framework import views

from . import models


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailySchedule
        fields = ('description',)


class Status(views.APIView):
    model = models.DailySchedule

    def get_object(self, time):
        try:
            return self.model.objects.get(start_time__lte=time,
                                          end_time__gte=time)
        except self.model.DoesNotExist:
            self.model(description='')

    @method_decorator(auth_decorators.login_required)
    def get(self, request):
        """:return: server's time with period description
        """
        now = timezone.localtime(timezone.now())
        _time = now.timetz()
        schedule_obj = self.get_object(_time)
        serializer = StatusSerializer(schedule_obj, many=False)
        status_info = serializer.data
        status_info.update({'hour': _time.hour, 'minute': _time.minute,
                            'second': _time.second})
        return response.Response(status_info, status=status.HTTP_200_OK)
