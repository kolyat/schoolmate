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

from testutils import settings
from school import models as school_models
from account import models as account_models
from . import _db_data


class Command(base.BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        # Clean up
        account_models.SchoolUser.objects.all().delete()
        school_models.SchoolSubject.objects.all().delete()
        school_models.SchoolForm.objects.all().delete()
        # Create new data
        [school_models.SchoolForm(form_number=n, form_letter=l).save()
         for n in school_models.FORM_NUMBERS.__reversed__()
         for l in _db_data.FORM_LETTERS]
        [school_models.SchoolSubject(subject=s).save()
         for s in _db_data.SUBJECTS]
        account_models.SchoolUser.objects.create_superuser(
            username=settings.ADMIN_USER,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASS
        )
