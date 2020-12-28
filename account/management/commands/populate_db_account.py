# Schoolmate - school management system
# Copyright (C) 2018-2021  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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


def prepare_account():
    """Generate account data
    """
    print('Create data for ACCOUNT app:')
    print('    {:.<25}...'.format('Superuser "{}"'.format(
        settings.USER_ADMIN['username'])), end='', flush=True)
    account_models.SchoolUser.objects.create_superuser(
        username=settings.USER_ADMIN['username'],
        password=settings.USER_ADMIN['password'],
        email=settings.USER_ADMIN['email']
    )  # Python 3.4.4 support
    print('OK')
    student = copy.deepcopy(settings.USER_STUDENT)
    print('    {:.<25}...'.format('User "{}"'.format(
        student['username'])), end='', flush=True)
    form_number = school_models.FormNumber.objects.get(
        number=student['school_form']['form_number'])
    form_letter = school_models.FormLetter.objects.get(
        letter=student['school_form']['form_letter'])
    school_form = school_models.SchoolForm.objects.get(
        form_number=form_number, form_letter=form_letter)
    student['school_form'] = school_form
    account_models.SchoolUser.objects.create_user(
        username=student['username'],
        password=student['password'],
        email=student['email'],
        first_name=student['first_name'],
        patronymic_name=student['patronymic_name'],
        last_name=student['last_name'],
        birth_date=student['birth_date'],
        school_form=student['school_form'],
        is_superuser=student['is_superuser'],
        is_staff=student['is_staff'],
        is_active=student['is_active']
    )  # Python 3.4.4 support
    print('OK')


class Command(base.BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        prepare_account()
