from django.conf import settings


MODEL_HITCOUNT = getattr(settings, 'HITCOUNT_HITCOUNT_MODEL', 'hitcount.HitCount')
