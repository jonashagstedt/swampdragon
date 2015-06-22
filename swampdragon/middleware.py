from django.utils.six import add_metaclass
from abc import abstractmethod, ABCMeta


@add_metaclass(ABCMeta)
class BasicMiddleware(object):

    """MiddleWare Interface for SwampDragon

    Inheriting Classes should implement process_request method

    Returns:
            None (might  change in future)
    """

    def __init__(self):
        pass

    @abstractmethod
    def process_request(self, connection, data):
        pass
