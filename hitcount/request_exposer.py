from django.conf import settings

from . import models


def RequestExposerMiddleware(get_response):
    def middleware(request):
        models.exposed_request = request
        response = get_response(request)
        return response

    return middleware
