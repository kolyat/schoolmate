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

from schoolmate import settings


PERIOD_NUMBERS = range(1, 9)
DAY_PERIOD_TYPES = (
    ('L', _('Lesson')),
    ('B', _('Break'))
)
YEAR_PERIOD_TYPES = (
    ('Q', _('Quarter')),
    ('H', _('Holidays'))
)


class FormLetter(models.Model):
    """School form's parallel
    """
    letter = models.CharField(
        blank=False,
        null=False,
        max_length=2,
        choices=tuple(zip(settings.FORM_LETTERS, settings.FORM_LETTERS)),
        verbose_name=_('Form letter')
    )

    def __str__(self):
        return self.letter

    def __unicode__(self):
        return self.letter

    class Meta:
        ordering = ('letter',)
        verbose_name = _('Form letter')
        verbose_name_plural = _('Form letters')


class FormNumber(models.Model):
    """Year № of education
    """
    number = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        choices=tuple(zip(
            settings.FORM_NUMBERS,
            [str(n) for n in settings.FORM_NUMBERS]
        )),
        verbose_name=_('Form number')
    )
    letters = models.ManyToManyField(
        FormLetter,
        through='SchoolForm',
        verbose_name='Form letter'
    )

    def __str__(self):
        return str(self.number)

    def __unicode__(self):
        return str(self.number)

    class Meta:
        ordering = ('number',)
        verbose_name = _('Form number')
        verbose_name_plural = _('Form numbers')


class SchoolForm(models.Model):
    """Represents school form
    """
    form_number = models.ForeignKey(
        FormNumber,
        on_delete=models.PROTECT,
        verbose_name='Form number'
    )
    form_letter = models.ForeignKey(
        FormLetter,
        on_delete=models.PROTECT,
        verbose_name='Form letter'
    )

    def __str__(self):
        return f'{self.form_number}{self.form_letter}'

    def __unicode__(self):
        return f'{self.form_number}{self.form_letter}'

    class Meta:
        ordering = ('form_number', 'form_letter')
        verbose_name = _('School form')
        verbose_name_plural = _('School forms')


class SchoolSubject(models.Model):
    """Represents school subject
    """
    subject = models.CharField(
        blank=True,
        null=False,
        unique=True,
        max_length=254,
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
    """Represents daily schedule:
    - period type (lesson/break)
    - number of a period
    - start & end time of a period
    """
    number = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        choices=tuple(zip(PERIOD_NUMBERS, [str(n) for n in PERIOD_NUMBERS])),
        verbose_name=_('Number of a period')
    )
    period_type = models.CharField(
        blank=False,
        null=False,
        max_length=2,
        choices=DAY_PERIOD_TYPES,
        verbose_name=_('Period type')
    )
    start_time = models.TimeField(
        blank=False,
        null=False,
        verbose_name=_('Start time of a period')
    )
    end_time = models.TimeField(
        blank=False,
        null=False,
        verbose_name=_('End time of a period')
    )
    description = models.CharField(
        blank=False,
        null=False,
        max_length=254,
        verbose_name=_('Additional description')
    )

    def __str__(self):
        return self.description

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _('Period')
        verbose_name_plural = _('Daily schedule')


class SchoolYear(models.Model):
    """Represents school year and it's duration
    """
    name = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=254,
        verbose_name=_('Name of school year')
    )
    start_date = models.DateField(
        blank=False,
        null=False,
        verbose_name=_('Start date of a school year')
    )
    end_date = models.DateField(
        blank=False,
        null=False,
        verbose_name=_('End date of a school year')
    )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('School year')
        verbose_name_plural = _('Academic years')


class YearSchedule(models.Model):
    """Represents schedule of a school year:
    - period type (academic quarter/holidays)
    - number of a period
    - start & end date of a period
    """
    school_year = models.ForeignKey(
        SchoolYear,
        on_delete=models.PROTECT,
        verbose_name=_('School year')
    )
    number = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        choices=tuple(zip(PERIOD_NUMBERS, [str(n) for n in PERIOD_NUMBERS])),
        verbose_name=_('Number of a period')
    )
    period_type = models.CharField(
        blank=False,
        null=False,
        max_length=2,
        choices=YEAR_PERIOD_TYPES,
        verbose_name=_('Period type')
    )
    start_date = models.DateField(
        blank=False,
        null=False,
        verbose_name=_('Start date of a period')
    )
    end_date = models.DateField(
        blank=False,
        null=False,
        verbose_name=_('End date of a period')
    )
    description = models.CharField(
        blank=False,
        null=False,
        max_length=254,
        verbose_name=_('Additional description')
    )

    def __str__(self):
        return self.description

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _('School year schedule')
        verbose_name_plural = _('Academic year schedules')


class Classroom(models.Model):
    """Represents classroom in a school building
    """
    room_id = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=15,
        verbose_name=_('Classroom ID')
    )
    room_name = models.CharField(
        blank=True,
        null=True,
        max_length=254,
        verbose_name=_('Classroom name')
    )

    def __str__(self):
        return self.room_id

    def __unicode__(self):
        return self.room_id

    class Meta:
        verbose_name = _('Classroom')
        verbose_name_plural = _('Classrooms')
