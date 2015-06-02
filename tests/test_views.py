# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from datetime import timedelta

try:
    import unittest.mock as mock
except ImportError:
    import mock

try:
    from importlib import import_module
except ImportError:  # prior to 1.7
    from django.utils.importlib import import_module

try:
    from django.test import override_settings
except ImportError:  # prior to 1.7
    from django.test.utils import override_settings

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User, Group
from django.http import Http404
from django.test import TestCase, RequestFactory
from django.utils import timezone

from hitcount.models import HitCount, BlacklistIP, BlacklistUserAgent
from hitcount.views import _update_hit_count, update_hit_count_ajax

from .models import Post


class UpdateHitCountTests(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title='my title', content='my text')
        self.hit_count = HitCount.objects.create(content_object=self.post)
        self.factory = RequestFactory()
        self.request = self.factory.get('/', REMOTE_ADDR="127.0.0.1",
            HTTP_USER_AGENT='my_clever_agent')

        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.request.session = store

        self.request.user = AnonymousUser()

    def test_anonymous_user_hit(self):
        """
        Test AnonymousUser Hit
        """
        response = _update_hit_count(self.request, self.hit_count)

        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: session key')

    def test_anonymous_user_hit_not_counted(self):
        """
        Test Multiple AnonymousUser Hit, not counted
        """

        response = _update_hit_count(self.request, self.hit_count)
        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: session key')

        response = _update_hit_count(self.request, self.hit_count)
        self.assertFalse(response.hit_counted)
        self.assertEqual(response.hit_message,
            'Not counted: session key has active hit')

    def test_anonymous_user_hit_counted_after_filter_active(self):
        """
        Test Multiple AnonymousUser Hit, counted because of filter active
        """
        # create a Hit ten days ago
        created = timezone.now() - timedelta(days=10)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = created

            response = _update_hit_count(self.request, self.hit_count)

        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: session key')

        # test a Hit today, within the filter time
        response = _update_hit_count(self.request, self.hit_count)
        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: session key')

    def test_registered_user_hit(self):
        """
        Test AnonymousUser Hit
        """
        self.request.user = User.objects.create_user('john',
            'lennon@thebeatles.com', 'johnpassword')
        response = _update_hit_count(self.request, self.hit_count)

        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message,
            'Hit counted: user authentication')

    def test_registered_user_hit_not_counted(self):
        """
        Test Multiple AnonymousUser Hit, not counted
        """
        self.request.user = User.objects.create_user('john',
            'lennon@thebeatles.com', 'johnpassword')

        response = _update_hit_count(self.request, self.hit_count)
        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message,
            'Hit counted: user authentication')

        response = _update_hit_count(self.request, self.hit_count)
        self.assertFalse(response.hit_counted)
        self.assertEqual(response.hit_message,
            'Not counted: authenticated user has active hit')

    def test_registered_user_hit_counted_after_filter_active(self):
        """
        Test Multiple AnonymousUser Hit, counted because of filter active
        """
        self.request.user = User.objects.create_user('john',
            'lennon@thebeatles.com', 'johnpassword')

        # create a Hit ten days ago
        created = timezone.now() - timedelta(days=10)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = created

            response = _update_hit_count(self.request, self.hit_count)

        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: user authentication')

        # test a Hit today, within the filter time
        response = _update_hit_count(self.request, self.hit_count)
        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: user authentication')

    @override_settings(HITCOUNT_HITS_PER_IP_LIMIT=2)
    def test_hits_per_ip_limit(self):
        """
        Test `HITCOUNT_HITS_PER_IP_LIMIT` setting.  Should allow multiple hits
        from the same IP until the limit is reached from that IP.
        """
        responses = []
        for x in range(3):
            # need a new session key each time.
            engine = import_module(settings.SESSION_ENGINE)
            store = engine.SessionStore()
            store.save()
            self.request.session = store
            responses.append(_update_hit_count(self.request, self.hit_count))

        self.assertTrue(responses[0].hit_counted)
        self.assertEqual(responses[0].hit_message, 'Hit counted: session key')
        self.assertTrue(responses[1].hit_counted)
        self.assertEqual(responses[1].hit_message, 'Hit counted: session key')
        self.assertFalse(responses[2].hit_counted)
        self.assertEqual(responses[2].hit_message,
            'Not counted: hits per IP address limit reached')
        hit_count = HitCount.objects.get(pk=1)
        self.assertEqual(hit_count.hits, 2)

    @override_settings(HITCOUNT_EXCLUDE_USER_GROUP=('Admin',))
    def test_exclude_user_group(self):
        """
        Exclude user by adding a group setting.
        """
        self.request.user = User.objects.create_user('john',
            'lennon@thebeatles.com', 'johnpassword')
        group = Group.objects.create(name='Admin')
        group.user_set.add(self.request.user)

        response = _update_hit_count(self.request, self.hit_count)
        self.assertFalse(response.hit_counted)
        self.assertEqual(response.hit_message,
            'Not counted: user excluded by group')

    def test_blacklist_ip(self):
        """
        Test black listed IPs.
        """
        BlacklistIP.objects.create(ip="127.0.0.1")

        response = _update_hit_count(self.request, self.hit_count)
        self.assertFalse(response.hit_counted)
        self.assertEqual(response.hit_message,
            'Not counted: user IP has been blacklisted')

    def test_blacklist_user_agent(self):
        """
        Test black listed user agents.
        """
        BlacklistUserAgent.objects.create(user_agent="my_clever_agent")

        response = _update_hit_count(self.request, self.hit_count)
        self.assertFalse(response.hit_counted)
        self.assertEqual(response.hit_message,
            'Not counted: user agent has been blacklisted')


class UpdateHitCountJSONTests(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title='my title', content='my text')
        self.hit_count = HitCount.objects.create(content_object=self.post)
        self.factory = RequestFactory()
        self.request = self.factory.post('/', {'hitcountPK': self.hit_count.pk},
            REMOTE_ADDR="127.0.0.1",
            HTTP_USER_AGENT='my_clever_agent',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.request.session = store

        self.request.user = AnonymousUser()

    def test_require_ajax(self):
        """
        Test require ajax request or raise 404
        """
        non_ajax_request = self.factory.get('/')
        with self.assertRaises(Http404):
            update_hit_count_ajax(non_ajax_request)

    def test_require_post_only(self):
        """
        Test require POST request or raise 404
        """
        non_ajax_request = self.factory.get('/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = update_hit_count_ajax(non_ajax_request)
        json_response = json.loads(response.content.decode())
        json_expects = json.loads('{"error_message": '
            '"Hits counted via POST only.", "success": false}')
        self.assertEqual(json_response, json_expects)

    def test_count_hit(self):
        """
        Test a valid request.
        """
        response = update_hit_count_ajax(self.request)
        self.assertEqual(response.content,
            b'[true, "Hit counted: session key"]')

    def test_count_hit_invalid_hitcount_pk(self):
        """
        Test a valid request with an invalid hitcount pk.
        """
        request = self.factory.post('/', {'hitcountPK': 15},
            REMOTE_ADDR="127.0.0.1",
            HTTP_USER_AGENT='my_clever_agent',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = update_hit_count_ajax(request)
        self.assertEqual(response.content,
            b'HitCount object_pk not working')
