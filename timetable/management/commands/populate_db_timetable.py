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

import random
from django.core.management import base

from school import models as school_models
from timetable import models as timetable_models
from school.management.commands import _db_data


class Command(base.BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        print('TIMETABLE app')
        print('Clean up... ', end='')
        timetable_models.Timetable.objects.all().delete()
        timetable_models.TimetableSchoolForm.objects.all().delete()
        print('OK')
        print('Create new data:')
        print('    {:.<25}...'.format('School forms in timetable'), end='')
        _year = school_models.SchoolYear.objects.get(
            name=_db_data.SCHOOL_YEAR['name'])
        _timetable_year = timetable_models.TimetableYear(school_year=_year)
        _timetable_year.save()
        _forms = school_models.SchoolForm.objects.all()
        _timetable_forms = [timetable_models.TimetableSchoolForm(
            year=_timetable_year, school_form=f) for f in _forms]
        [f.save() for f in _timetable_forms]
        print('OK')
        print('    {:.<25}...'.format('Timetable'), end='')
        _subjects = school_models.SchoolSubject.objects.all()
        random.seed()
        for tt_form in _timetable_forms:
            for d in timetable_models.DAYS_OF_WEEK:
                lessons = range(1, random.randint(6, 8))
                for l in lessons:
                    s = random.choice(_subjects)
                    timetable_models.Timetable(
                        form=tt_form, day_of_week=d[0],
                        lesson_number=l, subject=s
                    ).save()
        print('OK')