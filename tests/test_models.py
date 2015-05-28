# -*- coding: utf-8 -*-

from datetime import timedelta

try:
    import unittest.mock as mock
except ImportError:
    import mock

from django.test import TestCase
from django.utils import timezone

from hitcount.models import Hit, HitCount, BlacklistIP, BlacklistUserAgent

from .models import Post


class BlacklistUserAgentTests(TestCase):

    def test_string_representation(self):
        """
        Basic __str__ testing

        """
        ua_text = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4)"
        ua = BlacklistUserAgent(user_agent=ua_text)
        self.assertEqual(ua.__str__(), ua_text)


class BlacklistIPTests(TestCase):

    def test_string_representation(self):
        """
        Basic __str__ testing

        """
        ip_text = "127.0.0.1"
        ip = BlacklistIP(ip=ip_text)
        self.assertEqual(ip.__str__(), ip_text)


class HitTests(TestCase):

    def setUp(self):
        post = Post.objects.create(title='my title', content='my text')
        hit_count = HitCount.objects.create(content_object=post)
        self.hit = Hit.objects.create(hitcount=hit_count)

    def test_string_representation(self):
        """
        Basic __str__ testing

        """
        self.assertEqual(self.hit.__str__(), 'Hit: 1')

    def test_hit_count_increase(self):
        """
        Testing if Hit creation triggers increase of associated HitCount

        """
        hit_count = HitCount.objects.get(pk=1)
        self.assertEqual(hit_count.hits, 1)
        Hit.objects.create(hitcount=hit_count)
        hit_count = HitCount.objects.get(pk=1)
        self.assertEqual(hit_count.hits, 2)

    def test_hit_delete(self):
        """
        Testing if Hit deletion triggers decrease of associated HitCount

        """
        self.hit.delete()
        hit_count = HitCount.objects.get(pk=1)
        self.assertEqual(hit_count.hits, 0)

    def test_hit_delete_save_hitcount(self):
        """
        Testing if Hit deletion with `save_hitcount` flag preserves
        the associated HitCount

        """
        self.hit.delete(save_hitcount=True)
        hit_count = HitCount.objects.get(pk=1)
        self.assertEqual(hit_count.hits, 1)

    def test_filter_active(self):
        """
        Test for "active" Hits.  Out of ten, should have seven remaining.

        """
        hit_count = HitCount.objects.get(pk=1)

        # add 9 more Hits
        for x in xrange(1, 10):
            created = timezone.now() - timedelta(days=x)
            with mock.patch('django.utils.timezone.now') as mock_now:
                mock_now.return_value = created

                Hit.objects.create(hitcount=hit_count)

        self.assertEqual(len(Hit.objects.all()), 10)
        self.assertEqual(len(Hit.objects.filter_active()), 7)


class HitCountTests(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title='my title', content='my text')

    def test_string_representation(self):
        """
        Basic __str__ testing

        """
        post = Post.objects.create(title='my title', content='my text')
        hit_count = HitCount(content_object=post)
        self.assertEqual(hit_count.__str__(), 'Post title: my title')

    def test_increase(self):
        """
        Testing HitCount.increase()

        """
        hit_count = HitCount.objects.create(content_object=self.post)
        hit_count.increase()

        hit_count = HitCount.objects.get(pk=1)
        self.assertEqual(hit_count.hits, 1)

    def test_decrease(self):
        """
        Testing HitCount.decrease()

        """
        hit_count = HitCount.objects.create(hits=1, content_object=self.post)
        hit_count.decrease()

        hit_count = HitCount.objects.get(pk=1)
        self.assertEqual(hit_count.hits, 0)

    def test_hits_in_last_assert_error_when_no_args(self):
        """
        When no args presented for `hits_in_last` should raise an AssertionError.

        """
        hit_count = HitCount.objects.create(content_object=self.post)
        with self.assertRaises(AssertionError):
            hit_count.hits_in_last()

    def test_hits_in_last(self):
        """
        Test `hits_in_last` function.

        """
        hit_count = HitCount.objects.create(content_object=self.post)

        for x in xrange(0, 10):
            created = timezone.now() - timedelta(days=x * 5)
            with mock.patch('django.utils.timezone.now') as mock_now:
                mock_now.return_value = created

                Hit.objects.create(hitcount=hit_count)

        hit_count = HitCount.objects.get(pk=1)

        self.assertEqual(hit_count.hits_in_last(days=30), 6)

    def test_get_for_object(self):
        """
        Test `HitCountManager.get_for_object()`

        """
        post2 = Post.objects.create(title='my title2', content='my text')
        hit_count = HitCount.objects.create(content_object=self.post)
        hit_count2 = HitCount.objects.create(content_object=post2)
        self.assertEqual(HitCount.objects.get_for_object(self.post), hit_count)
        self.assertEqual(HitCount.objects.get_for_object(post2), hit_count2)
