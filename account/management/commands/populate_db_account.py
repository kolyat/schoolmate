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

import datetime

from django.core.management import base

from school import models as school_models
from account import models as account_models


def prepare_account():
    """Generate account data
    """
    print('Create data for ACCOUNT app:')
    print('    {:.<25}...'.format('Superuser "admin"'), end='', flush=True)
    account_models.SchoolUser.objects.create_superuser(
        username='admin',
        password='nimda',
        email='admin@school.edu'
    )
    print('OK')
    print('    {:.<25}...'.format('User "sam"'), end='', flush=True)
    form_number = school_models.FormNumber.objects.get(number=9)
    form_letter = school_models.FormLetter.objects.get(letter='Б')
    school_form = school_models.SchoolForm.objects.get(
        form_number=form_number, form_letter=form_letter)
    account_models.SchoolUser.objects.create_user(
        username='sam',
        password='sam',
        email='sam@school.edu',
        first_name='Sam',
        patronymic_name='J.',
        last_name='Smith',
        birth_date=datetime.datetime.now(),
        school_form=school_form,
        is_superuser=False,
        is_staff=False,
        is_active=True
    )
    print('OK')


class Command(base.BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        prepare_account()
