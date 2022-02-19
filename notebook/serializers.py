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

from rest_framework import serializers

from . import models


class Note(serializers.ModelSerializer):
    class Meta:
        model = models.NotebookRecord
        fields = ['pk', 'date_modified', 'title']


class NoteCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.NotebookRecord
        fields = ['pk', 'user', 'date_modified', 'title', 'text']
        read_only_fields = ['pk', 'date_modified']


class NoteRetrieve(serializers.ModelSerializer):
    class Meta:
        model = models.NotebookRecord
        fields = ['pk', 'date_modified', 'title', 'text']


class NoteUpdate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.NotebookRecord
        fields = ['pk', 'user', 'title', 'text']
        read_only_fields = ['pk', 'user']
