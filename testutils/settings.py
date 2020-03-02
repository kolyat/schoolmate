import logging
import datetime

#
# Logging
#
LOG_OPTIONS = {
    'filemode': 'a',
    'format': '%(asctime)s [%(module)15s] %(levelname)7s - %(funcName)s'
              ' - %(message)s',
    'level': logging.INFO
}

#
# Credentials
#
USER_ADMIN = {
    'username': 'admin',
    'password': 'nimda',
    'email': 'admin@school.edu'
}
USER_STUDENT = {
    'username': 'sam',
    'password': 'sam',
    'email': 'sam@school.edu',
    'first_name': 'Sam',
    'patronymic_name': 'J.',
    'last_name': 'Smith',
    'birth_date': datetime.datetime.now(),
    'school_form': {'form_number': 9, 'form_letter': 'Б'},
    'is_superuser': False,
    'is_staff': False,
    'is_active': True
}

#
# Endpoints
#
PROTOCOL = 'http://'
HOST = 'localhost:8000'
BASE_URL = ''.join((PROTOCOL, HOST))

LOGIN_PATH = '/profile/login/'
LOGIN_URL = ''.join((BASE_URL, LOGIN_PATH))

LOGOUT_PATH = '/profile/logout/'
LOGOUT_URL = ''.join((BASE_URL, LOGOUT_PATH))

PROFILE_PATH = '/profile/'
PROFILE_URL = ''.join((BASE_URL, PROFILE_PATH))

USER_INFO_PATH = '/profile/user/info/'

NEWS_PATH = '/news/'

STATUS_PATH = '/main/status/'
SCHOOL_FORMS_PATH = '/main/forms/'
SCHEDULE_YEAR_PATH = '/main/schedule/year/'
SCHEDULE_DAY_PATH = '/main/schedule/day/'
SCHOOL_SUBJECTS_PATH = '/main/subjects/'

TIMETABLE_DATA_PATH = '/timetable/data/'

DIARY_PATH = '/diary/'
DIARY_URL = ''.join((BASE_URL, DIARY_PATH))
