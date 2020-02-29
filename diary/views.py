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

import datetime
import collections
import copy

from django import shortcuts
from django.core import exceptions
from django.contrib.auth import decorators as auth_decorators
from django.views.decorators import http as http_decorators
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from rest_framework import views, serializers, response, status

from . import models
from account import models as account_models
from school import models as school_models
from timetable import models as tt_models


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def diary(request):
    """Diary page
    """
    return shortcuts.render(request, 'diary.html.j2')


class TimetableRecordSerializer(serializers.ModelSerializer):
    lesson_num = serializers.IntegerField(source='lesson_number')
    subject = serializers.StringRelatedField()

    class Meta:
        model = tt_models.Timetable
        fields = ('lesson_num', 'subject')


class RecordRetrieveSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    subject = serializers.StringRelatedField()

    class Meta:
        model = models.DiaryRecord
        fields = ('date', 'lesson_number', 'subject', 'text')


class RecordWriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=False, many=False,
        queryset=account_models.SchoolUser.objects.all()
    )
    date = serializers.DateField()
    subject = serializers.PrimaryKeyRelatedField(
        read_only=False, many=False,
        queryset=school_models.SchoolSubject.objects.all()
    )

    class Meta:
        model = models.DiaryRecord
        fields = ('user', 'date', 'lesson_number', 'subject', 'text')


@method_decorator(auth_decorators.login_required, name='dispatch')
class Record(views.APIView):
    """Interface for operating with diary records
    """
    model = models.DiaryRecord

    def get(self, request, *args, **kwargs):
        """Retrieve timetable and records for specified date

        :param request: client's request
        :param kwargs: 'year', 'month', 'day'

        :return: 200 OK
        :return: 424 FAILED DEPENDENCY; if user is not assigned to any
                 of school forms
        """
        _date = datetime.date(kwargs['year'], kwargs['month'], kwargs['day'])
        # Get timetable from requested date
        _form = account_models.SchoolUser.objects.get(
            username=request.user).school_form
        if _form == None:
            return response.Response(
                {'school_form': _('Current user is not assigned '
                                  'to any of school forms')},
                status=status.HTTP_424_FAILED_DEPENDENCY
            )
        params = {'form__year__school_year__start_date__lte': _date,
                  'form__year__school_year__end_date__gte': _date,
                  'form__school_form': _form,
                  'day_of_week': _date.weekday()+2}
        tt_object = tt_models.Timetable.objects.filter(**params)
        tt_serializer = TimetableRecordSerializer(tt_object, many=True)
        tt_data = tt_serializer.data
        # Get diary records from requested date
        params = {'user': request.user, 'date': _date}
        rec_object = self.model.objects.filter(**params)
        rec_serializer = RecordRetrieveSerializer(rec_object, many=True)
        rec_data = rec_serializer.data
        rec_data_dict = {
            it['lesson_number']: {'subject': it['subject'], 'text': it['text']}
            for it in rec_data
        }
        # Combine timetable with diary records
        response_data = []
        for i in range(1, 8):
            item = collections.OrderedDict()
            item.update({'id': i})
            item.update({'date': _date})
            item.update({'lesson_number': i})
            subjects = ' / '.join(
                [it['subject'] for it in tt_data if it['lesson_num'] == i])
            if subjects == '':
                subjects = ' '
            item.update({'subject': subjects})
            item.update({'text': ''})
            if rec_data_dict.get(i, None):
                item.update({'subject': rec_data_dict[i]['subject']})
                item.update({'text': rec_data_dict[i]['text']})
            item.update({'marks': ''})
            item.update({'signature': ''})
            response_data.append(item)
        return response.Response(response_data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Create/update diary record

        :param request: client's request
        :param kwargs: 'year', 'month', 'day'

        :return: 400 BAD REQUEST; school subject does not exist, serializer
                 errors
        :return: 201 CREATED; new record
        :return: 202 ACCEPTED; update existing record
        """
        _date = datetime.date(kwargs['year'], kwargs['month'], kwargs['day'])
        _data = copy.deepcopy(request.data)
        _lesson_number = _data.get('lesson_number', None)
        if _lesson_number == None:
            return response.Response(
                {'lesson_number': _('Number of lesson must be specified')},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif not _lesson_number.isdigit():
            return response.Response(
                {'lesson_number': _('Must be integer')},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif (int(_lesson_number) < 1) or (int(_lesson_number) > 7):
            return response.Response(
                {'lesson_number': _('Must be in range from 1 to 7 inclusive')},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            pass
        _data.update({'date': _date, 'user': request.user.id})
        subject_name = _data.get('subject', None)
        try:
            subject_id = school_models.SchoolSubject.objects.get(
                subject__exact=subject_name).id
        except exceptions.ObjectDoesNotExist:
            return response.Response(
                {'subject': _('Given school subject does not exist')},
                status=status.HTTP_400_BAD_REQUEST
            )
        _data['subject'] = subject_id
        try:
            record = self.model.objects.get(
                user__exact=request.user, date=_date,
                lesson_number=_lesson_number
            )
        except exceptions.ObjectDoesNotExist:
            record = None
        if record:
            serializer = RecordWriteSerializer(record, data=_data)
            _status = status.HTTP_202_ACCEPTED
        else:
            serializer = RecordWriteSerializer(data=_data)
            _status = status.HTTP_201_CREATED
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response_data['subject'] = subject_name
            response_data['user'] = request.user.username
        else:
            _status = status.HTTP_400_BAD_REQUEST
            response_data = serializer.errors
        return response.Response(response_data, status=_status)
