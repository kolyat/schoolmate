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

import copy

from django.core.management import base

from testutils import settings
from school import models as school_models
from account import models as account_models


class Command(base.BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        print('ACCOUNT app')
        print('Create new data:')
        print('    {:.<25}...'.format('Users'), end='', flush=True)
        account_models.SchoolUser.objects.create_superuser(
            **settings.USER_ADMIN)
        student = copy.deepcopy(settings.USER_STUDENT)
        form = student.pop('school_form')
        form_number = school_models.FormNumber.objects.get(
            number=form['form_number'])
        form_letter = school_models.FormLetter.objects.get(
            letter=form['form_letter'])
        school_form = school_models.SchoolForm.objects.get(
            form_number=form_number, form_letter=form_letter)
        account_models.SchoolUser.objects.create_user(
            **student, school_form=school_form)
        print('OK')
