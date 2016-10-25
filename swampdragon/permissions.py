from abc import ABCMeta, abstractmethod
from django.utils import six


def login_required(func):
    def not_logged_in(self, **kwargs):
        self.send_login_required({'signin_required': 'you need to sign in'})
        return

    def check_user(self, **kwargs):
        user = self.connection.user
        if not user:
            return not_logged_in(self, **kwargs)
        return func(self, **kwargs)
    return check_user


class RoutePermission(six.with_metaclass(ABCMeta, object)):
    @abstractmethod
    def test_permission(self, handler, verb, **kwargs):
        pass

    @abstractmethod
    def permission_failed(self, handler):
        pass


class LoginRequired(RoutePermission):
    def __init__(self, verbs=None):
        self.test_against_verbs = verbs

    def test_permission(self, handler, verb, **kwargs):
        if not self.test_against_verbs:
            return handler.connection.user is not None
        if self.test_against_verbs:
            if verb not in self.test_against_verbs:
                return True
        user = handler.connection.user
        return user is not None

    def permission_failed(self, handler):
        handler.send_login_required()
