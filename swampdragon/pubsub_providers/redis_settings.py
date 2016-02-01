from django.conf import settings

redis_host = None
redis_port = None
redis_db = None
redis_password = None


def get_redis_host():
    global redis_host
    if not redis_host:
        redis_host = getattr(settings, 'SWAMP_DRAGON_REDIS_HOST', 'localhost')
    return redis_host


def get_redis_port():
    global redis_port
    if not redis_port:
        redis_port = getattr(settings, 'SWAMP_DRAGON_REDIS_PORT', 6379)
    return redis_port


def get_redis_db():
    global redis_db
    if not redis_db:
        redis_db = getattr(settings, 'SWAMP_DRAGON_REDIS_DB', 0)
    return redis_db


def get_redis_password():
    global redis_password
    if not redis_password:
        redis_password = getattr(settings, 'SWAMP_DRAGON_REDIS_PASSWORD', None)
    return redis_password


def is_redis_sentinel():
    global redis_sentinel
    if not redis_sentinel:
        redis_sentinel = getattr(settings, 'SWAMP_DRAGON_REDIS_SENTINEL_MODE', False)
    return redis_sentinel

def get_redis_sentinel_master():
    global redis_sentinel_master
    if not redis_sentinel_master:
        redis_sentinel_master = getattr(settings, 'SWAMP_DRAGON_REDIS_SENTINEL_MASTER', 'mymaster') # default master name
    return redis_sentinel_master
