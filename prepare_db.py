import os
import shutil

from schoolmate.settings import BASE_DIR


APPS = ('school', 'account', 'timetable')


if __name__ == '__main__':
    # TODO: database re-creation procedure
    dirs = [os.path.join(BASE_DIR, app, 'migrations') for app in APPS]
    [shutil.rmtree(d) for d in dirs]
    [os.mkdir(d) for d in dirs]
    [open(os.path.join(d, '__init__.py'), 'w').close() for d in dirs]
    [os.system('manage.py makemigrations {}'.format(a)) for a in APPS]
    os.system('manage.py migrate')
    os.system('manage.py populate_db')
