from django import template
from dwampdragon.settings import dragon_settings

register = template.Library()


@register.simple_tag()
def swampdragon_settings():
    root_url = dragon_settings.DRAGON_URL
    if not root_url.endswith('/'):
        root_url += '/'
    return '<script type="text/javascript" src="{}settings.js"></script>'.format(root_url)
