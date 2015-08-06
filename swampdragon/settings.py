# the bulk of this was copied from django rest framework, but was tweaked since
# swampdragon doesn't namespace the settings.  Also updated to check
# environment variables before using defaults.
from __future__ import unicode_literals

import os
import importlib

from django.conf import settings
from django.utils import six


DEFAULTS = {
    # TODO: break up SWAMP_DRAGON_CONNECTION so it can be added to IMPORT_STRINGS
    'SWAMP_DRAGON_CONNECTION': ('swampdragon.connections.sockjs_connection.DjangoSubscriberConnection', '/data'),
    'SWAMP_DRAGON_HEARTBEAT_ENABLED': False,
    'SWAMP_DRAGON_HEARTBEAT_FREQUENCY': 1000 * 60 * 20,  # 20 minutes
    'SWAMP_DRAGON_SESSION_STORE': 'swampdragon.sessions.redis_session_store.RedisSessionStore',
    'SWAMP_DRAGON_REDIS_HOST': 'localhost',
    'SWAMP_DRAGON_REDIS_PORT': 6379,
    'SWAMP_DRAGON_REDIS_DB': 0,
    'SWAMP_DRAGON_HOST': '127.0.0.1',
    'SWAMP_DRAGON_PORT': 9999,
    'SWAMP_DRAGON_SAME_ORIGIN': False,
    'DRAGON_URL': 'http://localhost:9999/',
    'SWAMPDRAGON_TESTMODE': False,
    'SWAMP_DRAGON_PUBLISHER_CLASS': 'swampdragon.pubsub_providers.redis_publisher.RedisPublisher',
    'SWAMP_DRAGON_PUBLISHER_MOCK_CLASS': 'swampdragon.pubsub_providers.mock_publisher.MockPublisher',
    'SWAMP_DRAGON_SUBSCRIBER_CLASS': 'swampdragon.pubsub_providers.redis_sub_provider.RedisSubProvider',
    'SWAMP_DRAGON_SUBSCRIBER_MOCK_CLASS': 'swampdragon.pubsub_providers.mock_sub_provider.MockSubProvider',
    'SESSION_EXPIRATION_TIME': 30,
}


# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    'SWAMP_DRAGON_SESSION_STORE',
    'SWAMP_DRAGON_PUBLISHER_CLASS',
    'SWAMP_DRAGON_PUBLISHER_MOCK_CLASS',
    'SWAMP_DRAGON_SUBSCRIBER_CLASS',
    'SWAMP_DRAGON_SUBSCRIBER_MOCK_CLASS',
)


MOCK_ALIASES = {
    'SWAMP_DRAGON_PUBLISHER_CLASS': 'SWAMP_DRAGON_PUBLISHER_MOCK_CLASS',
    'SWAMP_DRAGON_SUBSCRIBER_CLASS': 'SWAMP_DRAGON_SUBSCRIBER_MOCK_CLASS',
}


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, six.string_types):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '%s' for setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class Settings(object):
    def __init__(self, defaults=None, import_strings=None):
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid setting: '%s'" % attr)

        if attr in MOCK_ALIASES.keys() and self.SWAMPDRAGON_TESTMODE:
            attr = MOCK_ALIASES[attr]

        try:
            # Check if present in settings
            val = getattr(settings, attr)
        except AttributeError:
            # Fall back to environment variables or defaults
            val = os.environ.get(attr, self.defaults[attr])

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        setattr(self, attr, val)
        return val


dragon_settings = Settings(DEFAULTS, IMPORT_STRINGS)
