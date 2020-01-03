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

from django.urls import path
from django.views import generic

from . import views


urlpatterns = [
    path('main/', views.index, name='index'),
    path('', generic.RedirectView.as_view(url='/main')),

    # API
    path('main/status/', views.Status.as_view()),
    path('main/forms/', views.Forms.as_view()),
    path('main/schedule/year/', views.YearScheduleView.as_view()),
    path('main/schedule/day/', views.DailyScheduleView.as_view()),
]
