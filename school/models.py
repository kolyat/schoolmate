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

PERIOD_NUMBERS = range(1, 9)
DAY_PERIOD_TYPES = (
    ('L', _('Lesson')),
    ('B', _('Break'))
)
YEAR_PERIOD_TYPES = (
    ('Q', _('Quarter')),
    ('H', _('Holidays'))
)


class SchoolForm(models.Model):
    """Represents school form
    """
    form_number = models.PositiveSmallIntegerField(
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


class SchoolSubject(models.Model):
    """Represents school subject
    """
    subject = models.CharField(
        max_length=254, blank=False, null=False,
        verbose_name=_('School subject')
    )

    def __str__(self):
        return self.subject

    def __unicode__(self):
        return self.subject

    class Meta:
        verbose_name = _('School subject')
        verbose_name_plural = _('School subjects')


class DailySchedule(models.Model):
    """Represents daily schedule
    Period type (lesson/break), it's number, when it starts and ends
    """
    number = models.PositiveSmallIntegerField(
        blank=False, null=False,
        choices=tuple(zip(PERIOD_NUMBERS, [str(n) for n in PERIOD_NUMBERS])),
        verbose_name=_('Number of a period')
    )
    period_type = models.CharField(
        max_length=2, blank=False, null=False, choices=DAY_PERIOD_TYPES,
        verbose_name=_('Period type')
    )
    start_time = models.TimeField(
        blank=False, null=False, verbose_name=_('Start time of a period')
    )
    end_time = models.TimeField(
        blank=False, null=False, verbose_name=_('End time of a period')
    )
    description = models.CharField(
        max_length=254, blank=False, null=False,
        verbose_name=_('Additional description')
    )

    def __str__(self):
        return self.description

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _('Daily schedule')
        verbose_name_plural = _('List of daily schedules')


class SchoolYear(models.Model):
    """Represents school year and it's duration
    """
    name = models.CharField(
        max_length=254, blank=False, null=False, unique=True,
        verbose_name=_('Name of school year')
    )
    start_date = models.DateField(
        blank=False, null=False, verbose_name=_('Start date of a school year')
    )
    end_date = models.DateField(
        blank=False, null=False, verbose_name=_('End date of a school year')
    )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('School year')
        verbose_name_plural = _('List of school years')


class YearSchedule(models.Model):
    """Represents schedule of a school year
    Period type (academic quarter/holidays), it's number, date of start
    and end
    """
    school_year = models.ForeignKey(SchoolYear, on_delete=models.DO_NOTHING,
                                    verbose_name=_('School year'))
    number = models.PositiveSmallIntegerField(
        blank=False, null=False,
        choices=tuple(zip(PERIOD_NUMBERS, [str(n) for n in PERIOD_NUMBERS])),
        verbose_name=_('Number of a period')
    )
    period_type = models.CharField(
        max_length=2, blank=False, null=False, choices=YEAR_PERIOD_TYPES,
        verbose_name=_('Period type')
    )
    start_date = models.DateField(
        blank=False, null=False, verbose_name=_('Start date of a period')
    )
    end_date = models.DateField(
        blank=False, null=False, verbose_name=_('End date of a period')
    )
    description = models.CharField(
        max_length=254, blank=False, null=False,
        verbose_name=_('Additional description')
    )

    def __str__(self):
        return self.description

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _('School year schedule')
        verbose_name_plural = _('List of school year schedules')
