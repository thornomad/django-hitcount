# -*- coding: utf-8 -*-

from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.management.base import NoArgsCommand

from hitcount.models import Hit


class Command(NoArgsCommand):
    help = "Can be run as a cronjob or directly to clean out old Hits objects from the database."

    def handle_noargs(self, **options):
        from django.db import transaction

        grace = getattr(settings, 'HITCOUNT_KEEP_HIT_IN_DATABASE', {'days': 30})
        period = timezone.now() - timedelta(**grace)
        Hit.objects.filter(created__lt=period).delete()
        transaction.commit_unless_managed()
