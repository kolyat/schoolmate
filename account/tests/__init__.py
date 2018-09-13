import os
import logging

from django.conf import settings as django_settings
from schoolmate import settings as project_settings
from testutils import settings


logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '{}.log'.format(__name__)),
    **settings.LOG_OPTIONS
)
logging.getLogger(__name__).addHandler(logging.NullHandler())

django_settings.configure(default_settings=project_settings)
