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

from django.contrib import admin

from . import models


@admin.register(models.SchoolForm)
class SchoolFormAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SchoolSubject)
class SchoolSubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DailySchedule)
class DailyScheduleAdmin(admin.ModelAdmin):
    list_display = ('number', 'period_type', 'start_time', 'end_time',
                    'description')
    list_editable = ('period_type', 'start_time', 'end_time', 'description')
    ordering = ('start_time',)


# @admin.register(models.YearSchedule)
# class YearScheduleAdmin(admin.ModelAdmin):
#     list_display = ('school_year', 'number', 'period_type',
#                     'start_date', 'end_date', 'description')
#     list_editable = ('number', 'period_type', 'start_date', 'end_date',
#                      'description')
#     ordering = ('-school_year', 'start_date')


class YearScheduleInline(admin.TabularInline):
    model = models.YearSchedule
    fields = ('number', 'period_type', 'start_date', 'end_date', 'description')
    ordering = ('start_date',)
    extra = 0


@admin.register(models.SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    inlines = [YearScheduleInline, ]
    list_display = ('name', 'start_date', 'end_date')
    ordering = ('-start_date',)


@admin.register(models.Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'room_name')
    list_editable = ('room_name',)
    ordering = ('room_id',)
