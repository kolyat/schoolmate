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

from django.contrib import admin
from related_admin import RelatedFieldAdmin

from . import models


@admin.register(models.NotebookRecord)
class NotebookRecordAdmin(RelatedFieldAdmin):
    list_display = (
        'user__username', 'date_modified', 'title', 'text'
    )
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'title', 'text', 'date_modified'
    )
