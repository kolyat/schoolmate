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

from django.urls import path
from django.views import generic
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # Login/logout
    path('login/',
         auth_views.LoginView.as_view(template_name='login.html.j2'),
         name='login'),
    path('logout/', views.logout, name='logout'),

    # Password reset
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html.j2',
             email_template_name='password_reset_email.html',
             subject_template_name='password_reset_subj.txt',
             success_url='password_reset/sent/'
         ),
         name='password_reset'),
    path('password_reset/sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_sent.html.j2'),
         name='password_reset_sent'),
    path('password_reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html.j2',
             post_reset_login=False,
             success_url='password_reset/complete/'
         ),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html.j2'),
         name='password_reset_complete'),

    # Password change
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             success_url='/password_change/done/'),
         name='password_change'),
    path('password_change/done/', views.password_change_done,
         name='password_change_done'),

    # Profile
    path('profile/', views.account, name='account'),
    path('', generic.RedirectView.as_view(url='/profile')),
    path('login/undefined', generic.RedirectView.as_view(url='/profile')),

    # API
    path('profile/user/', views.user),
    path('profile/user/info', views.UserInfo.as_view())
]
