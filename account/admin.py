# Schoolmate - school management system
# Copyright (C) 2018-2019  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext as _

from . import models


@admin.register(models.SchoolUser)
class SchoolUserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (_('Credentials'), {
            'fields': ('username', 'password')
        }),
        (_('User info'), {
            'fields': ('first_name', 'patronymic_name', 'last_name',
                       'birth_date', 'school_form')
        }),
        (_('Contacts'), {
            'fields': ('email',)
        }),
        (_('Miscellaneous'), {
            'fields': ('language', 'date_joined')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions')
        })
    )
    list_display = ('username', 'first_name', 'last_name', 'school_form',
                    'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'patronymic_name', 'last_name',
                     'birth_date', 'email')
