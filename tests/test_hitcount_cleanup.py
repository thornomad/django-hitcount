# -*- coding: utf-8 -*-
#
from datetime import timedelta

try:
    import unittest.mock as mock
except ImportError:
    import mock

from django.utils import timezone
from django.core.management import call_command
from django.test import TestCase

from hitcount.models import HitCount, Hit
from .models import Post


class HitCountCleanUp(TestCase):

    def setUp(self):

        post = Post.objects.create(title='hi', content='some text')
        post.save()

        hit_count = HitCount.objects.create(content_object=post)
        hit_count.save()

        for x in xrange(0, 10):
            created = timezone.now() - timedelta(days=x * 5)
            with mock.patch('django.utils.timezone.now') as mock_now:
                mock_now.return_value = created

                hit = Hit.objects.create(hitcount=hit_count)
                hit.save()

    def test_remove_expired_hits(self):
        """There should be only 6 items remaining after cleanup."""
        call_command('hitcount_cleanup')
        self.assertEqual(len(Hit.objects.all()), 6)

    def test_preserve_hitcount(self):
        """Removing Hits should not decrease the total HitCount."""
        hit_count = HitCount.objects.get(pk=1)
        call_command('hitcount_cleanup')
        self.assertEqual(hit_count.hits, 10)
