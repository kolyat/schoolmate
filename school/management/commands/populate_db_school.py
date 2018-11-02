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

from django.core.management import base

from school import models as school_models
from . import _db_data


class Command(base.BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        print('SCHOOL app')
        print('Clean up... ', end='')
        school_models.Classroom.objects.all().delete()
        school_models.YearSchedule.objects.all().delete()
        school_models.SchoolYear.objects.all().delete()
        school_models.DailySchedule.objects.all().delete()
        school_models.SchoolSubject.objects.all().delete()
        school_models.SchoolForm.objects.all().delete()
        print('OK')
        print('Create new data:')
        print('    {:.<25}...'.format('School forms'), end='')
        [school_models.SchoolForm(form_number=n, form_letter=l).save()
         for n in school_models.FORM_NUMBERS.__reversed__()
         for l in _db_data.FORM_LETTERS]
        print('OK')
        print('    {:.<25}...'.format('School subjects'), end='')
        [school_models.SchoolSubject(subject=s).save()
         for s in _db_data.SUBJECTS]
        print('OK')
        print('    {:.<25}...'.format('Daily schedule'), end='')
        [school_models.DailySchedule(**d).save()
         for d in _db_data.DAILY_SCHEDULE]
        print('OK')
        print('    {:.<25}...'.format('Year schedule'), end='')
        _sy = school_models.SchoolYear(**_db_data.SCHOOL_YEAR)
        _sy.save()
        [school_models.YearSchedule(school_year=_sy, **y).save()
         for y in _db_data.YEAR_SCHEDULE]
        print('OK')
        print('    {:.<25}...'.format('Classrooms'), end='')
        [school_models.Classroom(**c).save() for c in _db_data.CLASSROOMS]
        print('OK')