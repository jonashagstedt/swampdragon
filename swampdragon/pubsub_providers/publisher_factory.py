from swampdragon.settings import dragon_settings

_publisher = None


def get_publisher():
    global _publisher
    if _publisher is None:
        _publisher = dragon_settings.SWAMP_DRAGON_PUBLISHER_CLASS()
    return _publisher
