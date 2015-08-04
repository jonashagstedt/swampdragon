import json


class MockPublisher(object):
    def __init__(self):
        self.subscribers = {}

    def publish(self, channel, message):
        subs = self.subscribers.get(channel)
        if not subs:
            return
        for subscriber in subs:
            if isinstance(message, str):
                message = json.dumps(message)
            subscriber.published_data.append(message)

    def _get_channels_from_subscriptions(self, base_channel):
        channels = [key for key in self.subscribers.keys() if key.startswith(base_channel)]
        return channels

    def get_channels(self, base_channel):
        return self._get_channels_from_subscriptions(base_channel)

    def subscribe(self, channels, subscriber):
        for c in channels:
            if c not in self.subscribers.keys():
                self.subscribers[c] = []
            self.subscribers[c].append(subscriber)

    def unsubscribe(self, channels, subscriber):
        if not isinstance(channels, list):
            return self.unsubscribe([channels], subscriber)
        for channel in channels:
            self.subscribers[channel].remove(subscriber)

        empty_channels = [k for (k, v) in self.subscribers.items() if not v]
        for k in empty_channels:
            del self.subscribers[k]

    def remove_subscriber(self, subscriber):
        channels = [c for c in self.subscribers if subscriber in self.subscribers[c]]
        self.unsubscribe(channels, subscriber)
