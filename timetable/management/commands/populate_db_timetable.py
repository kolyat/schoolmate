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

import random
from django.core.management import base

from school import models as school_models
from timetable import models as timetable_models
from school.management.commands import _db_data


def prepare_timetable(forms=None):
    print('TIMETABLE app')
    print('Create new data:')
    print('    {:.<25}...'.format('School forms in timetable'),
          end='', flush=True)
    _year = school_models.SchoolYear.objects.get(
        name=_db_data.SCHOOL_YEAR['name'])
    _timetable_year = timetable_models.TimetableYear(school_year=_year)
    _timetable_year.save()
    if forms:
        numbers = [school_models.FormNumber.objects.get(number=f)
                   for f in forms]
        _forms = school_models.SchoolForm.objects.filter(
            form_number__in=numbers)
    else:
        _forms = school_models.SchoolForm.objects.all()
    _timetable_forms = [timetable_models.TimetableSchoolForm(
        year=_timetable_year, school_form=f) for f in _forms]
    [f.save() for f in _timetable_forms]
    print('OK')
    print('    {:.<25}...'.format('Timetable'), end='', flush=True)
    _subjects = school_models.SchoolSubject.objects.all()
    _classrooms = school_models.Classroom.objects.all()
    random.seed()
    for tt_form in _timetable_forms:
        for d in timetable_models.DAYS_OF_WEEK:
            lessons = range(1, random.randint(6, 8))
            for l in lessons:
                while True:
                    s = random.choice(_subjects)
                    if str(s) != ' ':
                        break
                c = random.choice(_classrooms)
                timetable_models.Timetable(
                    form=tt_form, day_of_week=d[0], lesson_number=l,
                    subject=s, classroom=c
                ).save()
    print('OK')


class Command(base.BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        prepare_timetable()
