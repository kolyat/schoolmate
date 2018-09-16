import os
import logging

from testutils import settings


logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '{}.log'.format(__name__)),
    **settings.LOG_OPTIONS
)
logging.getLogger(__name__).addHandler(logging.NullHandler())
