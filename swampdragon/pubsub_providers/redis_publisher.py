import json
import redis
from swampdragon.settings import dragon_settings

_redis_cli = None


def get_redis_cli():
    global _redis_cli
    if not _redis_cli:
        _redis_cli = redis.StrictRedis(
            host=dragon_settings.SWAMP_DRAGON_REDIS_HOST,
            port=dragon_settings.SWAMP_DRAGON_REDIS_PORT,
            db=dragon_settings.SWAMP_DRAGON_REDIS_DB
        )
    return _redis_cli


class RedisPublisher(object):
    def publish(self, channel, message):
        get_redis_cli().publish(channel, json.dumps(message))

    def _get_channels_from_redis(self, base_channel):
        channels = get_redis_cli().execute_command('PUBSUB', 'channels', '{}*'.format(base_channel))
        return [c.decode() for c in channels]

    def get_channels(self, base_channel):
        return self._get_channels_from_redis(base_channel)
