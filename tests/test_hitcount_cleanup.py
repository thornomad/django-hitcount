# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

try:
    import unittest.mock as mock
except ImportError:
    import mock

from django.utils import timezone
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from hitcount.models import Hit
from hitcount.utils import get_hitcount_model
from blog.models import Post

COMMAND_NAME = 'hitcount_cleanup'

HitCount = get_hitcount_model()


class HitCountCleanUp(TestCase):

    def setUp(self):

        post = Post.objects.create(title='hi', content='some text')
        hit_count = HitCount.objects.create(content_object=post)

        for x in range(10):
            created = timezone.now() - timedelta(days=x * 5)
            with mock.patch('django.utils.timezone.now') as mock_now:
                mock_now.return_value = created

                Hit.objects.create(hitcount=hit_count)

    def test_remove_expired_hits(self):
        """There should be only 6 items remaining after cleanup."""
        call_command(COMMAND_NAME)
        self.assertEqual(len(Hit.objects.all()), 6)

    def test_preserve_hitcount(self):
        """Removing Hits should not decrease the total HitCount."""
        hit_count = HitCount.objects.get(pk=1)
        call_command(COMMAND_NAME)
        self.assertEqual(hit_count.hits, 10)

    def test_standard_output(self):
        out = StringIO()
        call_command(COMMAND_NAME, stdout=out)
        self.assertIn('Successfully removed 4 Hits', out.getvalue())
