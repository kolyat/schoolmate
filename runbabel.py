# Schoolmate - school management system
# Copyright (C) 2018-2023  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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
import sys
import argparse


APPS = (
    'school',
    'account',
    'news',
    'timetable',
    'diary',
    'notebook'
)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Babel launcher')
    parser.add_argument('-e', '--extract', action='store_true',
                        default=False, required=False,
                        help='get translation strings', dest='extract')
    parser.add_argument('-i', '--init', action='store_true',
                        default=False, required=False,
                        help='create/overwrite locale files', dest='init')
    parser.add_argument('-u', '--update', action='store_true',
                        default=False, required=False,
                        help='update locale files', dest='update')
    parser.add_argument('-o', '--compile', action='store_true',
                        default=False, required=False,
                        help='compile locale files', dest='compile')
    args = parser.parse_args()

    opts = ' --msgid-bugs-address=kks.pub@gmail.com ' \
           ' --copyright-holder="Kirill \'Kolyat\' Kiselnikov" ' \
           ' --project=Schoolmate ' \
           ' --version=2.0 '

    if args.extract:
        os.system(f'pybabel extract -F babelcfg/babel.common.cfg'
                  f' -o locale/django.pot {opts} .')
        for app in APPS:
            os.system(f'pybabel extract -F babelcfg/babel.{app}.cfg'
                      f' -o {app}/locale/django.pot {opts} .')

    if args.init:
        # os.system('pybabel init -D django -i locale/django.pot'
        #           ' -d locale -l ru')
        # os.system('pybabel init -D django -i locale/django.pot'
        #           ' -d locale -l de')
        # os.system('pybabel init -D django -i school/locale/django.pot'
        #           ' -d school/locale -l ru')
        # os.system('pybabel init -D django -i school/locale/django.pot'
        #           ' -d school/locale -l de')
        # os.system('pybabel init -D django -i account/locale/django.pot'
        #           ' -d account/locale -l ru')
        # os.system('pybabel init -D django -i account/locale/django.pot'
        #           ' -d account/locale -l de')
        # os.system('pybabel init -D django -i news/locale/django.pot'
        #           ' -d news/locale -l ru')
        # os.system('pybabel init -D django -i news/locale/django.pot'
        #           ' -d news/locale -l de')
        # os.system('pybabel init -D django -i timetable/locale/django.pot'
        #           ' -d timetable/locale -l ru')
        # os.system('pybabel init -D django -i timetable/locale/django.pot'
        #           ' -d timetable/locale -l de')
        # os.system('pybabel init -D django -i diary/locale/django.pot'
        #           ' -d diary/locale -l ru')
        # os.system('pybabel init -D django -i diary/locale/django.pot'
        #           ' -d diary/locale -l de')
        # os.system('pybabel init -D django -i notebook/locale/django.pot'
        #           ' -d notebook/locale -l ru')
        # os.system('pybabel init -D django -i notebook/locale/django.pot'
        #           ' -d notebook/locale -l de')
        pass

    if args.update:
        os.system('pybabel update -D django -i locale/django.pot -d locale'
                  ' --previous')
        for app in APPS:
            os.system(f'pybabel update -D django -i {app}/locale/django.pot'
                      f' -d {app}/locale --previous')

    if args.compile:
        os.system('pybabel compile -D django -d locale')
        for app in APPS:
            os.system(f'pybabel compile -D django -d {app}/locale')

    if len(sys.argv) < 2:
        print('Nothing to do')
        parser.print_usage()
