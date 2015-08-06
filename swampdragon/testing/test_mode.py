from swampdragon.settings import dragon_settings


def set_test_mode():
    dragon_settings.SWAMPDRAGON_TESTMODE = True


def test_mode():
    return dragon_settings.SWAMPDRAGON_TESTMODE
