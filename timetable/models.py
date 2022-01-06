# Schoolmate - school management system
# Copyright (C) 2018-2022  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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


DAYS_OF_WEEK = (
    (2, _('Monday')),
    (3, _('Tuesday')),
    (4, _('Wednesday')),
    (5, _('Thursday')),
    (6, _('Friday')),
    (7, _('Saturday'))
)
days_of_week = dict(DAYS_OF_WEEK)


class TimetableYear(models.Model):
    """Proxy model for school year
    """
    school_year = models.ForeignKey(
        school_models.SchoolYear, on_delete=models.PROTECT,
        verbose_name=_('School year')
    )

    def __str__(self):
        return str(self.school_year)

    def __unicode__(self):
        return str(self.school_year)

    class Meta:
        verbose_name = _('Timetable')
        verbose_name_plural = _('Timetable')


class TimetableSchoolForm(models.Model):
    """Link school year to school forms
    """
    year = models.ForeignKey(TimetableYear, on_delete=models.PROTECT,
                             verbose_name=_('Year'))
    school_form = models.ForeignKey(
        school_models.SchoolForm, on_delete=models.PROTECT,
        verbose_name=_('School form')
    )

    def __str__(self):
        return str(self.school_form)

    def __unicode__(self):
        return str(self.school_form)

    class Meta:
        ordering = ('school_form',)
        verbose_name = _('Form')
        verbose_name_plural = _('Form')


class Timetable(models.Model):
    """Represents timetable
    """
    form = models.ForeignKey(TimetableSchoolForm, on_delete=models.PROTECT,
                             verbose_name=_('Form'), related_name='lessons')
    day_of_week = models.PositiveSmallIntegerField(
        blank=False, null=False, choices=DAYS_OF_WEEK,
        verbose_name=_('Day of week')
    )
    lesson_number = models.PositiveSmallIntegerField(
        blank=False, null=False,
        choices=tuple(zip(school_models.PERIOD_NUMBERS,
                          [str(n) for n in school_models.PERIOD_NUMBERS])),
        verbose_name=_('Lesson number')
    )
    subject = models.ForeignKey(
        school_models.SchoolSubject, on_delete=models.PROTECT,
        verbose_name=_('Subject')
    )
    classroom = models.ForeignKey(
        school_models.Classroom, blank=True, null=True,
        on_delete=models.PROTECT, verbose_name=_('Classroom')
    )

    def __str__(self):
        return ' | '.join((days_of_week[self.day_of_week],
                           str(self.lesson_number),
                           str(self.subject)))

    def __unicode__(self):
        return ' | '.join((days_of_week[self.day_of_week],
                           str(self.lesson_number),
                           str(self.subject)))

    class Meta:
        ordering = ('day_of_week', 'lesson_number')
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
