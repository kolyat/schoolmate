import os
import sys
import argparse


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
           ' --version=0.1 '

    if args.extract:
        os.system('pybabel extract -F babelcfg/babel.common.cfg'
                  ' -o locale/django.pot {} .'.format(opts))
        os.system('pybabel extract -F babelcfg/babel.school.cfg'
                  ' -o school/locale/django.pot {} .'.format(opts))
        os.system('pybabel extract -F babelcfg/babel.account.cfg'
                  ' -o account/locale/django.pot {} .'.format(opts))
        os.system('pybabel extract -F babelcfg/babel.news.cfg'
                  ' -o news/locale/django.pot {} .'.format(opts))
        os.system('pybabel extract -F babelcfg/babel.timetable.cfg'
                  ' -o timetable/locale/django.pot {} .'.format(opts))

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
        pass

    if args.update:
        os.system('pybabel update -D django -i locale/django.pot -d locale'
                  ' --previous')
        os.system('pybabel update -D django -i school/locale/django.pot'
                  ' -d school/locale --previous')
        os.system('pybabel update -D django -i account/locale/django.pot'
                  ' -d account/locale --previous')
        os.system('pybabel update -D django -i news/locale/django.pot'
                  ' -d news/locale --previous')
        os.system('pybabel update -D django -i timetable/locale/django.pot'
                  ' -d timetable/locale --previous')

    if args.compile:
        os.system('pybabel compile -D django -d locale')
        os.system('pybabel compile -D django -d school/locale')
        os.system('pybabel compile -D django -d account/locale')
        os.system('pybabel compile -D django -d news/locale')
        os.system('pybabel compile -D django -d timetable/locale')

    if len(sys.argv) < 2:
        print('Nothing to do')
        parser.print_usage()
