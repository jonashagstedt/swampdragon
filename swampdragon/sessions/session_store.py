from abc import ABCMeta, abstractmethod
from django.utils import six


class BaseSessionStore(six.with_metaclass(ABCMeta, object)):
    def __init__(self, connection):
        self.connection = connection
        self.keys = []

    @abstractmethod
    def set(self, key, val):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def refresh_key_timeout(self, key):
        pass

    def refresh_all_keys(self):
        for key in self.keys:
            self.refresh_key_timeout(key)
