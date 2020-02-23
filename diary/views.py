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

from django import shortcuts
from django.core import exceptions
from django.core import serializers as renderers
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
    subject = serializers.StringRelatedField()

    class Meta:
        model = models.DiaryRecord
        fields = ('lesson_number', 'subject', 'text')


class RecordWriteSerializer(serializers.ModelSerializer):
    subject = serializers.PrimaryKeyRelatedField(
        read_only=False, many=False,
        queryset=school_models.SchoolSubject.objects.all()
    )

    class Meta:
        model = models.DiaryRecord
        fields = ('lesson_number', 'subject', 'text')


@method_decorator(auth_decorators.login_required, name='dispatch')
class Record(views.APIView):

    def get(self, request, *args, **kwargs):
        _date = datetime.date(kwargs['year'], kwargs['month'], kwargs['day'])
        # Get timetable from requested date
        _form = account_models.SchoolUser.objects.get(
            username=request.user).school_form
        try:
            _form_number = _form.form_number.number
            _form_letter = _form.form_letter.letter
        except AttributeError:
            return response.Response(
                {'error': _('Current user is not assigned to any of school forms')},
                status=status.HTTP_424_FAILED_DEPENDENCY
            )
        params = {'form__year__school_year__start_date__lte': _date,
                  'form__year__school_year__end_date__gte': _date,
                  'form__school_form__form_number__number': _form_number,
                  'form__school_form__form_letter__letter': _form_letter,
                  'day_of_week': _date.weekday()+2}
        object_tt = tt_models.Timetable.objects.filter(**params)
        serializer_tt = TimetableRecordSerializer(object_tt, many=True)
        data_tt = serializer_tt.data
        # Get diary records from requested date
        params = {'user': request.user, 'date': _date}
        object_rec = models.DiaryRecord.objects.filter(**params)
        serializer_rec = RecordRetrieveSerializer(object_rec, many=True)
        data_rec = serializer_rec.data
        # Combine timetable with diary records
        response_data = []
        data_rec_d = {
            it['lesson_number']: {'subject': it['subject'], 'text': it['text']}
            for it in data_rec
        }
        for i in range(1, 8):
            item = collections.OrderedDict()
            item.update({'id': i})
            item.update({'lesson_num': i})
            subjects = ' / '.join(
                [it['subject'] for it in data_tt if it['lesson_num'] == i])
            item.update({'subject': subjects})
            if data_rec_d.get(i, None):
                item.update({'subject': data_rec_d[i]['subject']})
                item.update({'record': data_rec_d[i]['text']})
            item.update({'marks': ''})
            item.update({'signature': ''})
            response_data.append(item)
        return response.Response(response_data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        _date = datetime.date(kwargs['year'], kwargs['month'], kwargs['day'])
        _data = request.data
        try:
            subj = school_models.SchoolSubject.objects.get(
                subject__exact=_data.get('subject', None))
            _data['subject'] = subj.id
        except exceptions.ObjectDoesNotExist:
            return response.Response(
                {'subject': _('Given school subject does not exist')},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RecordWriteSerializer(data=_data)
        if not serializer.is_valid():
            return response.Response(serializer.errors,
                                     status=status.HTTP_400_BAD_REQUEST)
        try:
            r = models.DiaryRecord.objects.get(
                user__exact=request.user, date=_date,
                lesson_number=serializer.validated_data['lesson_number']
            )
            r.subject = subj
            r.text = serializer.validated_data['text']
            r.save()
            return response.Response(renderers.serialize('json', (r,)),
                                     status=status.HTTP_202_ACCEPTED)
        except exceptions.ObjectDoesNotExist:
            serializer.save(user=request.user, date=_date)
            return response.Response(serializer.data,
                                     status=status.HTTP_201_CREATED)
