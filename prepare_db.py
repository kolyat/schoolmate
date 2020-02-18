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

import os
import shutil
from django.core import management


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmate.settings')
APPS = (
    'school',
    'account',
    'news',
    'timetable',
    'diary'
)


class Db(object):
    def __init__(self, db_info, project_root):
        self.db_info = db_info
        self.project_root = project_root
        if 'postgresql' in self.db_info['ENGINE']:
            import psycopg2
            self.connection = psycopg2.connect(
                user=db_info['USER'], password=db_info['PASSWORD'],
                host=db_info['HOST'], port=db_info['PORT']
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        else:
            from django.db import connection
            self.connection = connection
            self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def create(self):
        if 'sqlite' in self.db_info['ENGINE']:
            print('Re-creating SQLite database file "{}"...'
                  ''.format(self.db_info['NAME']), end=' ', flush=True)
            open(self.db_info['NAME'], mode='w').close()
            print('OK')
        else:
            print('Deleting database "{}"...'.format(self.db_info['NAME']),
                  end=' ', flush=True)
            self.cursor.execute('DROP DATABASE IF EXISTS {}'
                                ''.format(self.db_info['NAME']))
            print('OK')
            print('Re-creating database...', end=' ', flush=True)
            self.cursor.execute('CREATE DATABASE {} WITH ENCODING \'UTF8\''
                                ''.format(self.db_info['NAME']))
            print('OK')

    def remove_migrations(self, app):
        print('Re-creating migration directory for {}...'.format(app),
              end=' ', flush=True)
        _dir = os.path.join(self.project_root, app, 'migrations')
        if os.path.exists(_dir):
            shutil.rmtree(_dir)
        os.mkdir(_dir)
        open(os.path.join(_dir, '__init__.py'), 'w').close()
        print('OK')

    @staticmethod
    def make_migrations(app):
        management.call_command('makemigrations', app)

    @staticmethod
    def migrate(*args):
        management.call_command('migrate', *args)

    @staticmethod
    def clear(app):
        management.call_command('clear_db_{}'.format(app))

    @staticmethod
    def populate(app):
        management.call_command('populate_db_{}'.format(app))


if __name__ == '__main__':
    import django
    django.setup()
    from django.conf import settings
    db = Db(settings.DATABASES['default'], settings.BASE_DIR)
    db.create()
    for a in APPS:
        db.remove_migrations(a)
    for a in APPS:
        db.make_migrations(a)
    db.migrate()
    for a in APPS:
        db.populate(a)
