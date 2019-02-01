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

import os
import shutil

from schoolmate.settings import BASE_DIR, DATABASES


APPS = (
    'school',
    'account',
    'news',
    'timetable'
)


if __name__ == '__main__':
    db_info = DATABASES['default']
    if 'sqlite' in db_info['ENGINE']:
        print('Re-creating SQLite database file "{}"... '
              ''.format(db_info['NAME']), end='')
        open(db_info['NAME'], mode='w').close()
        print('OK')
    if 'postgresql' in db_info['ENGINE']:
        import psycopg2
        connection = psycopg2.connect(
            user=db_info['USER'], password=db_info['PASSWORD'],
            host=db_info['HOST'], port=db_info['PORT']
        )
        connection.autocommit = True
        cursor = connection.cursor()
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmate.settings')
        from django.db import connection
        cursor = connection.cursor()
    if 'sqlite' not in db_info['ENGINE']:
        print('Deleting database "{}"... '.format(db_info['NAME']), end='')
        cursor.execute('DROP DATABASE {}'.format(db_info['NAME']))
        print('OK')
        print('Re-creating database... ', end='')
        cursor.execute('CREATE DATABASE {} WITH ENCODING \'UTF8\''
                       ''.format(db_info['NAME']))
        print('OK')
    print('Re-creating migration directories... ', end='')
    dirs = [os.path.join(BASE_DIR, app, 'migrations') for app in APPS]
    [shutil.rmtree(d) if os.path.exists(d) else None for d in dirs]
    [os.mkdir(d) for d in dirs]
    [open(os.path.join(d, '__init__.py'), 'w').close() for d in dirs]
    print('OK')
    [os.system('manage.py makemigrations {}'.format(app)) for app in APPS]
    os.system('manage.py migrate')
    # [os.system('manage.py clear_db_{}'.format(app)) for app in reversed(APPS)]
    [os.system('manage.py populate_db_{}'.format(app)) for app in APPS]
