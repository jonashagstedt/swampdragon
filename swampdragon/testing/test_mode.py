import os
from django.conf import settings


def set_test_mode():
    os.environ.setdefault('SWAMPDRAGON_TESTMODE', 'True')


def test_mode():
    if os.environ.get('SWAMPDRAGON_TESTMODE') == 'True':
        return True

    if getattr(settings, 'SWAMPDRAGON_TESTMODE', False) is True:
        return True

    return False
