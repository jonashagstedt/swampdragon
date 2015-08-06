import uuid
from swampdragon.settings import dragon_settings


SAME_ORIGIN_COOKIE_NAME = 'sdso'


def test_origin(connection):
    if not dragon_settings.SWAMP_DRAGON_SAME_ORIGIN:
        return True

    if not hasattr(connection, SAME_ORIGIN_COOKIE_NAME):
        return False

    return True


def set_origin_cookie(request_handler):
    request_handler.set_cookie(SAME_ORIGIN_COOKIE_NAME, uuid.uuid4().hex)


def set_origin_connection(request, connection):
    if not dragon_settings.SWAMP_DRAGON_SAME_ORIGIN:
        return True

    so_cookie = request.get_cookie(SAME_ORIGIN_COOKIE_NAME)
    if not so_cookie:
        return False

    if not hasattr(connection, SAME_ORIGIN_COOKIE_NAME):
        setattr(connection, SAME_ORIGIN_COOKIE_NAME, so_cookie.value)

    return True
