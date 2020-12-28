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
from django.utils.translation import gettext as _

from account import models as account_models


class Article(models.Model):
    """News article
    """
    author = models.ForeignKey(
        account_models.SchoolUser, on_delete=models.DO_NOTHING,
        blank=True, null=True, editable=False, verbose_name=_('Author')
    )
    created = models.DateTimeField(blank=False, null=False, auto_now_add=True,
                                   verbose_name=_('Creation date'))
    modified = models.DateTimeField(blank=False, null=False, auto_now=True,
                                    verbose_name=_('Last modification date'))
    title = models.CharField(max_length=254, blank=True, null=True,
                             verbose_name=_('Title'))
    content = models.TextField(max_length=30000, blank=False, null=False,
                               verbose_name=_('Content'))

    def __str__(self):
        return self.title if self.title else self.content

    def __unicode__(self):
        return self.title if self.title else self.content

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Article')
        verbose_name_plural = _('News')
