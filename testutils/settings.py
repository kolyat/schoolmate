import logging

#
# Logging
#
LOG_OPTIONS = {
    'filemode': 'w',
    'format': '%(asctime)s [%(module)15s] %(levelname)7s - %(funcName)s'
              ' - %(message)s',
    'level': logging.INFO
}

#
# Credentials
#
ADMIN_USER = 'admin'
ADMIN_EMAIL = 'admin@school.edu'
ADMIN_PASS = 'nimda'

#
# Endpoints
#
PROTOCOL = 'http://'
HOST = 'localhost:8000'
BASE_URL = '{}{}'.format(PROTOCOL, HOST)

LOGIN_PATH = '/login/'
LOGIN_URL = '{}{}'.format(BASE_URL, LOGIN_PATH)

LOGOUT_PATH = '/logout/'
LOGOUT_URL = '{}{}'.format(BASE_URL, LOGOUT_PATH)
