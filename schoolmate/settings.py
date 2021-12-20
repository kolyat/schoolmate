# Schoolmate - school management system
# Copyright (C) 2018-2021  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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
from django.utils.translation import gettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'ewp4nk8ffbd+*07_ei%1@er8%4eh0%)-c-q)#jp9f2=u!872lj'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    # Django apps and Grappelli admin
    'django.contrib.contenttypes',
    'grappelli.dashboard',
    'grappelli',
    'related_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django plugins
    'django_jinja',
    'django_babel',
    'rest_framework',
    # Project apps
    'school.apps.SchoolConfig',
    'account.apps.AccountConfig',
    'news.apps.NewsConfig',
    'timetable.apps.TimetableConfig',
    'diary.apps.DiaryConfig'
]
MIDDLEWARE = [
    # Django middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom middleware
    'user_language_middleware.UserLanguageMiddleware',
    'django_babel.middleware.LocaleMiddleware',
    'account.middleware.skin.SkinMiddleware'
]
ROOT_URLCONF = 'schoolmate.urls'
TEMPLATES = [
    {
        'NAME': 'django_jinja',
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'autoescape': False,
            'match_extension': '.html.j2',
            # 'match_regex': r'^(?!admin/).*',
            'newstyle_gettext': True,
            'translation_engine': 'django.utils.translation',
            'extensions': [
                # 'jinja2.ext.do',
                'jinja2.ext.loopcontrols',
                # 'jinja2.ext.with_',
                'jinja2.ext.i18n',
                'jinja2.ext.autoescape',
                'django_jinja.builtins.extensions.CsrfExtension',
                'django_jinja.builtins.extensions.CacheExtension',
                'django_jinja.builtins.extensions.TimezoneExtension',
                'django_jinja.builtins.extensions.UrlsExtension',
                'django_jinja.builtins.extensions.StaticFilesExtension',
                'django_jinja.builtins.extensions.DjangoFiltersExtension'
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
            'constants': {}
        }
    },
    {
        'NAME': 'django_templates',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ]
        }
    }
]
WSGI_APPLICATION = 'schoolmate.wsgi.application'


# Database
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'schoolmate.db'
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'schoolmate',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


# E-mail settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'robot@school.edu'


# Password validation
AUTH_USER_MODEL = 'account.SchoolUser'

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # }
]

LOGIN_URL = '/profile/login/'
LOGIN_REDIRECT_URL = '/'


# Internationalization
LANGUAGES = (        # i =
    ('ru', 'Русский'),  # 0
    ('en', 'English'),  # 1
    ('de', 'Deutsch')   # 2
)
LANGUAGE_CODE = LANGUAGES[0][0]  # LANGUAGES[i][0]
TEMPLATES[0]['OPTIONS']['constants'].update({'server_lang': LANGUAGE_CODE})

LOCALE_PATHS = [
    os.path.join(BASE_DIR,              'locale'),
    os.path.join(BASE_DIR, 'school',    'locale'),
    os.path.join(BASE_DIR, 'account',   'locale'),
    os.path.join(BASE_DIR, 'news',      'locale'),
    os.path.join(BASE_DIR, 'timetable', 'locale'),
    os.path.join(BASE_DIR, 'diary',     'locale')
]

TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,              'static'),
    os.path.join(BASE_DIR, 'school',    'static'),
    os.path.join(BASE_DIR, 'account',   'static'),
    os.path.join(BASE_DIR, 'timetable', 'static'),
    os.path.join(BASE_DIR, 'diary',     'static')
]


# Grappelli settings
GRAPPELLI_ADMIN_TITLE = _('Schoolmate maintenance')
GRAPPELLI_INDEX_DASHBOARD = 'schoolmate.dashboard.SchoolmateAdminDashboard'
GRAPPELLI_AUTOCOMPLETE_LIMIT = 7
GRAPPELLI_SWITCH_USER = False
GRAPPELLI_SWITCH_USER_ORIGINAL = False
GRAPPELLI_SWITCH_USER_TARGET = False


# Miscellaneous
SKINS = (                   # i =
    ('compact',  'Compact'),   # 0
    ('contrast', 'Contrast'),  # 1
    ('flat',     'Flat'),      # 2
    ('material', 'Material'),  # 3
    ('mini',     'Mini')       # 4
)
DEFAULT_SKIN = SKINS[1][0]  # SKINS[i][0]
TEMPLATES[0]['OPTIONS']['constants'].update({'default_skin': DEFAULT_SKIN})

LATEST_NEWS_COUNT = 300
