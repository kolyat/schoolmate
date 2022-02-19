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

from account import models as account_models


class NotebookRecord(models.Model):
    """Represents notebook record
    """
    user = models.ForeignKey(
        account_models.SchoolUser,
        on_delete=models.CASCADE,
        verbose_name=_('Notebook record'),
        related_name='notebook_records'
    )
    title = models.CharField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name=_('Notebook record title')
    )
    text = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Notebook record text')
    )
    date_modified = models.DateTimeField(
        blank=False,
        null=False,
        auto_now=True,
        verbose_name=_('Record\'s date & time of modification')
    )

    def __str__(self):
        return self.title or str(self.date_modified)

    def __unicode__(self):
        return self.title or str(self.date_modified)

    class Meta:
        ordering = ('-date_modified',)
        verbose_name = _('Notebook record')
        verbose_name_plural = _('Notebook records')
