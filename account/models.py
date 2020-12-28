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

from django.db import models
from django.contrib.auth import models as auth_models
from django.utils.translation import gettext as _

from schoolmate import settings
from school import models as school_models


class SchoolUser(auth_models.AbstractUser):
    """Extended version of user model
    """
    patronymic_name = models.CharField(max_length=254, blank=True, null=True,
                                       verbose_name=_('Patronymic name'))
    birth_date = models.DateField(blank=True, null=True,
                                  verbose_name=_('Date of birth'))
    school_form = models.ForeignKey(
        school_models.SchoolForm, blank=True, null=True,
        on_delete=models.DO_NOTHING, verbose_name=_('School form')
    )
    language = models.CharField(
        max_length=9, blank=False, null=False,
        choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE,
        verbose_name=_('Language')
    )

    class Meta:
        verbose_name = _('School user')
        verbose_name_plural = _('School users')
