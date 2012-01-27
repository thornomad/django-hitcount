import datetime
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Can be run as a cronjob or directly to clean out old Hits objects from the database."

    def handle_noargs(self, **options):
        from django.db import transaction
        from hitcount.models import Hit
        from django.conf import settings
        grace = getattr(settings, 'HITCOUNT_KEEP_HIT_IN_DATABASE', {'days':30})
        period = datetime.datetime.now() - datetime.timedelta(**grace)
        Hit.objects.filter(created__lt=period).delete()
        transaction.commit_unless_managed()
