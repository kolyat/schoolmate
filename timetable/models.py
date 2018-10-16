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

from school import models as school_models


DAYS_OF_WEEK = (
    (2, _('Monday')),
    (3, _('Tuesday')),
    (4, _('Wednesday')),
    (5, _('Thursday')),
    (6, _('Friday')),
    (7, _('Saturday'))
)
days_of_week = dict(*DAYS_OF_WEEK)


class Timetable(models.Model):
    """Lesson schedule of each academic year
    """
    lesson_number = models.PositiveSmallIntegerField(
        blank=False, null=False,
        choices=tuple(zip(school_models.PERIOD_NUMBERS,
                          [str(n) for n in school_models.PERIOD_NUMBERS])),
        verbose_name=_('Lesson number')
    )
    classroom = models.OneToOneField(school_models.Classroom,
                                     on_delete=models.DO_NOTHING)
    subject = models.OneToOneField(school_models.SchoolSubject,
                                   on_delete=models.DO_NOTHING)
    day_of_week = models.PositiveSmallIntegerField(
        blank=False, null=False, choices=DAYS_OF_WEEK,
        verbose_name=_('Day of week')
    )
    year = models.OneToOneField(school_models.SchoolYear,
                                on_delete=models.DO_NOTHING)

    def __str__(self):
        return '-'.join((days_of_week[self.day_of_week],
                         str(self.lesson_number),
                         str(self.subject)))

    def __unicode__(self):
        return '-'.join((days_of_week[self.day_of_week],
                         str(self.lesson_number),
                         str(self.subject)))

    class Meta:
        verbose_name = _('Timetable')
        verbose_name_plural = _('Timetables')
