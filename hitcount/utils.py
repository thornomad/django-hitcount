import warnings

from ipaddress import ip_address as validate_ip
from hitcount import settings
from etc.toolbox import get_model_class_from_settings


def get_ip(request):
    """
    Retrieves the remote IP address from the request data.  If the user is
    behind a proxy, they may have a comma-separated list of IP addresses, so
    we need to account for that.  In such a case, only the first IP in the
    list will be retrieved.  Also, some hosts that use a proxy will put the
    REMOTE_ADDR into HTTP_X_FORWARDED_FOR.  This will handle pulling back the
    IP from the proper place.

    **NOTE** This function was taken from django-tracking (MIT LICENSE)
             http://code.google.com/p/django-tracking/
    """

    # if neither header contain a value, just use local loopback
    ip_address = request.headers.get('X-Forwarded-For',
                                  request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        # make sure we have one and only one IP
        try:
            validate_ip(ip_address)
        except ValueError:
            # no IP, probably from some dirty proxy or other device
            # throw in some bogus IP
            ip_address = '10.0.0.1'

    return ip_address


def get_hitcount_model():
    """Returns the HitCount model, set for the project."""
    return get_model_class_from_settings(settings, 'MODEL_HITCOUNT')


class RemovedInHitCount13Warning(DeprecationWarning):
    pass

# enable warnings by default for our deprecated
warnings.simplefilter("default", RemovedInHitCount13Warning)
