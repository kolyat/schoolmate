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

from django.db import models
from django.utils.translation import gettext as _


FORM_NUMBERS = range(1, 12)
FORM_LETTERS = 'АБВГД'


class SchoolForm(models.Model):
    """Represents school form
    """
    form_number = models.PositiveIntegerField(
        blank=False, null=False,
        choices=tuple(zip(FORM_NUMBERS, [str(n) for n in FORM_NUMBERS])),
        verbose_name=_('Form number')
    )
    form_letter = models.CharField(
        max_length=2, blank=False, null=False,
        choices=tuple(zip(FORM_LETTERS, FORM_LETTERS)),
        verbose_name=_('Form letter')
    )

    def __str__(self):
        return '{}{}'.format(self.form_number, self.form_letter)

    def __unicode__(self):
        return '{}{}'.format(self.form_number, self.form_letter)

    class Meta:
        verbose_name = _('School form')
        verbose_name_plural = _('School forms')
