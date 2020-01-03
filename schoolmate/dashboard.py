# Schoolmate - school management system
# Copyright (C) 2018-2020  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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

from django.utils.translation import gettext_lazy as _

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class SchoolmateAdminDashboard(Dashboard):
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        self.children.append(modules.ModelList(
            _('Administration'),
            column=1,
            collapsible=False,
            models=('account.models.SchoolUser', 'django.contrib.*')
        ))
        self.children.append(modules.Group(
            _('General'),
            column=1,
            collapsible=False,
            children=(
                modules.ModelList(
                    title='',
                    models=(
                        'school.models.SchoolForm',
                        'school.models.SchoolSubject',
                        'school.models.Classroom'
                    )
                ),
                modules.ModelList(
                    title='',
                    models=('news.models.Article',)
                ),
            )
        ))
        self.children.append(modules.ModelList(
            _('Schedules'),
            column=1,
            collapsible=False,
            models=(
                'school.models.DailySchedule',
                'school.models.SchoolYear',
                'timetable.models.TimetableYear'
            )
        ))
        self.children.append(modules.ModelList(
            _('Diary'),
            column=1,
            collapsible=False,
            models=(
                'diary.models.DiaryRecord',
            )
        ))
