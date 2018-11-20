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

from timetable import models as timetable_models


class Command(base.BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        print('TIMETABLE app')
        print('Clean up... ', end='')
        timetable_models.TimetableSubject.objects.all().delete()
        timetable_models.Timetable.objects.all().delete()
        timetable_models.TimetableSchoolForm.objects.all().delete()
        timetable_models.TimetableYear.objects.all().delete()
        print('OK')
