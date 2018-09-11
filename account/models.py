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

import itertools
from django.db import models
from django.contrib.auth import models as auth_models
from multiselectfield import MultiSelectField

from schoolmate import settings


FORM_NUMBERS = [str(n) for n in range(1, 12)]
FORM_LETTERS = 'АБВГД'
FORMS = [''.join(f) for f in itertools.product(FORM_NUMBERS, FORM_LETTERS)]


class SchoolUser(auth_models.AbstractUser):
    """Extended version of user model
    """
    patronymic_name = models.CharField(max_length=254, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    school_form = MultiSelectField(blank=True, null=True,
                                   choices=tuple(zip(FORMS, FORMS)))
    language = models.CharField(
        max_length=9, blank=False, null=False,
        choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE
    )
