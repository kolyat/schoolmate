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

import datetime
import collections
import copy

from django.template.response import TemplateResponse
from django.core import exceptions
from django.contrib.auth import decorators as auth_decorators
from django.views.decorators import http as http_decorators
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from rest_framework import views, response, status

from school import models as school_models
from timetable import models as tt_models
from . import models, serializers


@auth_decorators.login_required()
@http_decorators.require_http_methods(['GET'])
def diary(request):
    """Diary page
    """
    return TemplateResponse(request, 'diary.html.j2', context={})


@method_decorator(auth_decorators.login_required, name='dispatch')
class Record(views.APIView):
    """Interface for operating with diary records
    """
    model = models.DiaryRecord

    def get(self, request, *args, **kwargs):
        """Retrieve timetable with diary records for specified date.

        *Success response*: `200 OK`.

        *Error response*: `424 FAILED DEPENDENCY` if current user is not
        assigned to any of school forms.

        ```json
        [
            {
                "id": 1,
                "date": "2023-02-29",
                "lesson_number": 1,
                "subject": "Algebra",
                "text": "Some records here",
                "marks": "",
                "signature": ""
            },
            {
                "id": 2,
                "date": "2023-02-29",
                "lesson_number": 2,
                "subject": "Physics",
                "text": "",
                "marks": "",
                "signature": ""
            },
            {
                "id": 3,
                "date": "2023-02-29",
                "lesson_number": 3,
                "subject": "Chemistry",
                "text": "Some records here",
                "marks": "",
                "signature": ""
            },
            {
                "id": 4,
                "date": "2023-02-29",
                "lesson_number": 4,
                "subject": "Biology",
                "text": "",
                "marks": "",
                "signature": ""
            },
            {
                "id": 5,
                "date": "2023-02-29",
                "lesson_number": 5,
                "subject": "P.E.",
                "text": "",
                "marks": "",
                "signature": ""
            },
            {
                "id": 6,
                "date": "2023-02-29",
                "lesson_number": 6,
                "subject": " ",
                "text": "",
                "marks": "",
                "signature": ""
            },
            {
                "id": 7,
                "date": "2023-02-29",
                "lesson_number": 7,
                "subject": " ",
                "text": "",
                "marks": "",
                "signature": ""
            }
        ]
        ```
        """
        _date = datetime.date(kwargs['year'], kwargs['month'], kwargs['day'])

        # Get timetable from requested date
        if request.user.school_form is None:
            return response.Response(
                {'school_form': _('Current user is not assigned '
                                  'to any of school forms')},
                status=status.HTTP_424_FAILED_DEPENDENCY
            )
        params = {'form__year__school_year__start_date__lte': _date,
                  'form__year__school_year__end_date__gte': _date,
                  'form__school_form': request.user.school_form,
                  'day_of_week': _date.weekday()+2}
        tt_object = tt_models.Timetable.objects.filter(**params)
        tt_serializer = serializers.Timetable(tt_object, many=True)
        tt_data = tt_serializer.data

        # Get diary records from requested date
        params = {'user': request.user, 'date': _date}
        rec_object = self.model.objects.filter(**params)
        rec_serializer = serializers.DiaryRecordRead(rec_object, many=True)
        rec_data = rec_serializer.data
        rec_data_dict = {
            it['lesson_number']: {'subject': it['subject'], 'text': it['text']}
            for it in rec_data
        }

        # Combine timetable with diary records
        response_data = []
        for i in range(1, 8):
            item = collections.OrderedDict()
            item.update({'id': i, 'date': _date, 'lesson_number': i})
            subjects = ' / '.join(
                [it['subject'] for it in tt_data if it['lesson_num'] == i]
            )
            if subjects == '':
                subjects = ' '
            item.update({'subject': subjects, 'text': ''})
            if rec_data_dict.get(i, None):
                item.update({
                    'subject': rec_data_dict[i]['subject'],
                    'text': rec_data_dict[i]['text']
                })
            item.update({'marks': '', 'signature': ''})
            response_data.append(item)
        return response.Response(response_data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Create/update diary record.

        *Required data parameters*:
        - `lesson_number: integer`
        - `subject: string`
        - `text: string`

        *Success responses*:
        - New record: `201 CREATED`
        - Existing record updated: `202 ACCEPTED`

        ```json
        {
            "user": "sam",
            "date": "2023-02-29",
            "lesson_number": 3,
            "subject": "Chemistry",
            "text": "New records here"
        }
        ```

        *Error responses*: `400 BAD REQUEST`
        - `{"lesson_number": "Number of lesson must be specified"}`
        - `{"lesson_number": "Must be integer"}`
        - `{"lesson_number": "Must be in range from 1 to 7 inclusive"}`
        - `{"subject": "Given school subject does not exist"}`
        """
        _date = datetime.date(kwargs['year'], kwargs['month'], kwargs['day'])
        _data = copy.deepcopy(request.data)
        _data.update({'date': _date, 'user': request.user.id})
        subject_name = _data.get('subject', None)
        try:
            subject_id = school_models.SchoolSubject.objects.get(
                subject__exact=subject_name
            ).id
        except exceptions.ObjectDoesNotExist:
            return response.Response(
                {'subject': _('Given school subject does not exist')},
                status=status.HTTP_400_BAD_REQUEST
            )
        _data['subject'] = subject_id
        serializers.DiaryRecordWrite(data=_data).is_valid(raise_exception=True)
        try:
            record = self.model.objects.get(
                user__exact=request.user, date=_date,
                lesson_number=_data['lesson_number']
            )
            _status = status.HTTP_202_ACCEPTED
        except exceptions.ObjectDoesNotExist:
            record = None
            _status = status.HTTP_201_CREATED
        serializer = serializers.DiaryRecordWrite(instance=record, data=_data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response_data['subject'] = subject_name
            response_data['user'] = request.user.username
        else:
            _status = status.HTTP_400_BAD_REQUEST
            response_data = serializer.errors
        return response.Response(response_data, status=_status)
