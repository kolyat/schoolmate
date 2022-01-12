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

from rest_framework import viewsets


class MultipleSerializerGenericViewSet(viewsets.GenericViewSet):
    """Extension of GenericViewSet that supports multiple serializers for each
    action. Dictionary with 'action-serializer' pair is stored in 'serializers'
    property:
    serializers = {
        'create': CreateUpdateSerializer,
        'retrieve': RetrieveSerializer,
        ...
    }
    Overrides get_serializer_class(), returns defined serializer based on
    current action. If serializer is not found, returns 'serializer_class' as a
    default.
    """
    serializers = {}

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializer_class)
