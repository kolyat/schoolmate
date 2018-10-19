import os
import shutil

from schoolmate.settings import BASE_DIR, DATABASES


APPS = ('school', 'account', 'timetable')


if __name__ == '__main__':
    db_info = DATABASES['default']
    if 'postgresql' in DATABASES['default']['ENGINE']:
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
    cursor.execute('DROP DATABASE {}'.format(db_info['NAME']))
    cursor.execute('CREATE DATABASE {} WITH ENCODING \'UTF8\''
                   ''.format(db_info['NAME']))
    dirs = [os.path.join(BASE_DIR, app, 'migrations') for app in APPS]
    [shutil.rmtree(d) for d in dirs]
    [os.mkdir(d) for d in dirs]
    [open(os.path.join(d, '__init__.py'), 'w').close() for d in dirs]
    [os.system('manage.py makemigrations {}'.format(a)) for a in APPS]
    os.system('manage.py migrate')
    os.system('manage.py populate_db')
