# Schoolmate - school management system
# Copyright (C) 2018-2023  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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

from school import models as school_models
from account import models as account_models


class DiaryRecord(models.Model):
    """Represents diary record
    """
    user = models.ForeignKey(
        account_models.SchoolUser,
        on_delete=models.CASCADE,
        verbose_name=_('Diary record'),
        related_name='diary_records'
    )
    date = models.DateField(
        blank=False,
        null=False,
        verbose_name=_('Date')
    )
    lesson_number = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        choices=tuple(zip(
            school_models.PERIOD_NUMBERS,
            [str(n) for n in school_models.PERIOD_NUMBERS]
        )),
        verbose_name=_('Lesson number')
    )
    subject = models.ForeignKey(
        school_models.SchoolSubject,
        on_delete=models.DO_NOTHING,
        verbose_name=_('Subject')
    )
    text = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Diary record text')
    )

    def __str__(self):
        return ' | '.join((
            str(self.user),
            str(self.date),
            str(self.lesson_number),
            str(self.subject),
            self.text
        ))

    def __unicode__(self):
        return ' | '.join((
            str(self.user),
            str(self.date),
            str(self.lesson_number),
            str(self.subject),
            self.text
        ))

    class Meta:
        ordering = ('date',)
        verbose_name = _('Diary record')
        verbose_name_plural = _('Diary records')
