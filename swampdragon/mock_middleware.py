from .middleware import BasicMiddleware


class TestMiddleware(BasicMiddleware):

    """
    Middleware sets 'dummy' variable in the connection
    """

    def __init__(self):
        super(TestMiddleware, self).__init__()

    def process_request(self, connection, data):
        connection.dummy = True
