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

from django.template.response import TemplateResponse
from django.contrib.auth import decorators as auth_decorators
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import mixins

from utils import misc
from . import models, serializers


@method_decorator(auth_decorators.login_required, name='dispatch')
class Notebook(View):
    def get(self, request):
        return TemplateResponse(request, 'notebook.html.j2', context={})


@method_decorator(auth_decorators.login_required, name='dispatch')
class Record(mixins.CreateModelMixin,
             mixins.ListModelMixin,
             misc.MultipleSerializerGenericViewSet):
    serializer_class = serializers.Note
    serializers = {
        'create': serializers.NoteCreate,
        'list': serializers.Note
    }

    def get_queryset(self):
        return models.NotebookRecord.objects.filter(
            user__username=self.request.user)


@method_decorator(auth_decorators.login_required, name='dispatch')
class Note(mixins.RetrieveModelMixin,
           mixins.UpdateModelMixin,
           mixins.DestroyModelMixin,
           misc.MultipleSerializerGenericViewSet):
    serializer_class = serializers.NoteRetrieve
    serializers = {
        'retrieve': serializers.NoteRetrieve,
        'update': serializers.NoteUpdate
    }

    def get_queryset(self):
        return models.NotebookRecord.objects.filter(
            user__username=self.request.user)
