from sockjs.tornado import SockJSConnection
from tornado.ioloop import PeriodicCallback
from django.conf import settings
from swampdragon.settings import dragon_settings
from ..pubsub_providers.subscriber_factory import get_subscription_provider
from .. import route_handler
from ..same_origin import set_origin_connection, test_origin
import json


class ConnectionMixin(object):
    def to_json(self, data):
        """
        If the message is a dict, return it.
        If it's a string try to decode it into json,
        otherwise assume it's not a dictionary but a simple text message
        """
        if isinstance(data, dict):
            return data
        try:
            return json.loads(data)
        except:
            return {'message': data}


class SubscriberConnection(ConnectionMixin, SockJSConnection):
    pub_sub = None

    def __init__(self, session):
        super(SubscriberConnection, self).__init__(session)
        self.session_store = dragon_settings.SWAMP_DRAGON_SESSION_STORE(self)
        self.pub_sub = get_subscription_provider()

    def _close_invalid_origin(self):
        self.close(4000, message='Invalid origin')

    def on_open(self, request):
        if not set_origin_connection(request, self):
            self._close_invalid_origin()
            return

        super(SubscriberConnection, self).on_open(request)
        if dragon_settings.SWAMP_DRAGON_HEARTBEAT_ENABLED:
            self.periodic_callback = PeriodicCallback(self.send_heartbeat, dragon_settings.SWAMP_DRAGON_HEARTBEAT_FREQUENCY)
            self.periodic_callback.start()

    def send_heartbeat(self):
        self.send({'heartbeat': '1'})

    def on_heartbeat(self):
        self.session_store.refresh_all_keys()

    def on_close(self):
        if hasattr(self, 'periodic_callback'):
            self.periodic_callback.stop()
        self.pub_sub.close(self)

    def on_message(self, data):
        if not test_origin(self):
            self._close_invalid_origin()

        try:
            data = self.to_json(data)
            if data == {'heartbeat': '1'}:
                self.on_heartbeat()
                return
            handler = route_handler.get_route_handler(data['route'])
            handler(self).handle(data)
        except Exception as e:
            if settings.DEBUG:
                print(e)
            self.abort_connection()
            raise e

    def abort_connection(self):
        self.close(code=3001, message='Connection aborted')

    def close(self, code=3000, message='Connection closed'):
        self.session.close(code, message)


class DjangoSubscriberConnection(SubscriberConnection):
    pass
