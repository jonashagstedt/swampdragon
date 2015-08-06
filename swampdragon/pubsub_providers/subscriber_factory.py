from swampdragon.settings import dragon_settings


_subscriber = None


# only here for backwards compatibility
def get_subscription_provider():
    global _subscriber
    if _subscriber is None:
        _subscriber = dragon_settings.SWAMP_DRAGON_SUBSCRIBER_CLASS()
    return _subscriber
