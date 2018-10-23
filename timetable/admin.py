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

from django.contrib import admin

from . import models


class TimetableInline(admin.TabularInline):
    model = models.Timetable
    fields = ('day_of_week', 'lesson_number', 'subject', 'classroom')
    ordering = ('day_of_week', 'lesson_number')
    extra = 0


class TimetableSchoolFormInline(admin.StackedInline):
    model = models.TimetableSchoolForm
    show_change_link = True
    fields = ('school_form',)
    ordering = ('-school_form',)
    extra = 0


@admin.register(models.TimetableYear)
class TimetableYearAdmin(admin.ModelAdmin):
    inlines = (TimetableSchoolFormInline,)
    fields = ('school_year',)
    ordering = ('school_year',)


@admin.register(models.TimetableSchoolForm)
class TimetableSchoolFormAdmin(admin.ModelAdmin):
    inlines = (TimetableInline,)
    fields = ('school_form',)
    ordering = ('-school_form',)

    def has_module_permission(self, request):
        return False
