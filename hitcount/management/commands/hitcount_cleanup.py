# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.management.base import NoArgsCommand

from hitcount.models import Hit


class Command(NoArgsCommand):
    help = "Can be run as a cronjob or directly to clean out old Hits objects from the database."

    def handle_noargs(self, **options):
        grace = getattr(settings, 'HITCOUNT_KEEP_HIT_IN_DATABASE', {'days': 30})
        period = timezone.now() - timedelta(**grace)
        qs = Hit.objects.filter(created__lt=period)
        number_removed = len(qs)
        qs.delete()
        self.stdout.write('Successfully removed %s Hits' % number_removed)
