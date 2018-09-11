import os
import sys
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Babel launcher')
    parser.add_argument('-c', '--create', action='store_true',
                        default=False, required=False,
                        help='create locale files', dest='create')
    parser.add_argument('-u', '--update', action='store_true',
                        default=False, required=False,
                        help='update locale files', dest='update')
    parser.add_argument('-o', '--compile', action='store_true',
                        default=False, required=False,
                        help='compile locale files', dest='compile')
    args = parser.parse_args()

    if args.create:
        os.system('pybabel extract -F babelcfg/babel.common.cfg'
                  ' -o locale/django.pot .')
        os.system('pybabel init -D django -i locale/django.pot'
                  ' -d locale -l ru')
        os.system('pybabel init -D django -i locale/django.pot'
                  ' -d locale -l de')
        os.system('pybabel extract -F babelcfg/babel.account.cfg'
                  ' -o account/locale/django.pot .')
        os.system('pybabel init -D django -i account/locale/django.pot'
                  ' -d account/locale -l ru')
        os.system('pybabel init -D django -i account/locale/django.pot'
                  ' -d account/locale -l de')

    if args.update:
        os.system('pybabel update -D django -i locale/django.pot -d locale')
        os.system('pybabel update -D django -i account/locale/django.pot'
                  ' -d account/locale')

    if args.compile:
        os.system('pybabel compile -D django -d locale')
        os.system('pybabel compile -D django -d account/locale')

    if len(sys.argv) < 2:
        print('Nothing to do')
        parser.print_usage()
