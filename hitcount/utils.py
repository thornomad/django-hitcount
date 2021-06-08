from __future__ import unicode_literals
import re
import warnings
from hitcount import settings
from etc.toolbox import get_model_class_from_settings
IP_RE = re.compile('\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}')


def get_ip(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get(
        'REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        try:
            ip_address = IP_RE.match(ip_address)
            if ip_address:
                ip_address = ip_address.group(0)
            else:
                ip_address = '10.0.0.1'
        except IndexError:
            pass
    return ip_address


def get_hitcount_model():
    return get_model_class_from_settings(settings, 'MODEL_HITCOUNT')


class RemovedInHitCount13Warning(DeprecationWarning):
    pass


warnings.simplefilter('default', RemovedInHitCount13Warning)
