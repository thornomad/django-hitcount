# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import warnings
import json
from datetime import timedelta

try:
    import unittest.mock as mock
except ImportError:
    import mock

from importlib import import_module

from django.test import override_settings
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User, Group
from django.http import Http404
from django.test import TestCase, RequestFactory
from django.utils import timezone

from hitcount.models import BlacklistIP, BlacklistUserAgent
from hitcount.views import HitCountMixin, HitCountJSONView, HitCountDetailView
from hitcount.views import _update_hit_count, update_hit_count_ajax
from hitcount.utils import RemovedInHitCount13Warning, get_hitcount_model

from blog.models import Post

HitCount = get_hitcount_model()


class HitCountTestBase(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title='my title', content='my text')
        self.hit_count = HitCount.objects.create(content_object=self.post)
        self.factory = RequestFactory()
        self.request_post = self.factory.post(
            '/',
            {'hitcountPK': self.hit_count.pk},
            REMOTE_ADDR="127.0.0.1",
            HTTP_USER_AGENT='my_clever_agent',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.request_get = self.factory.get(
            '/',
            REMOTE_ADDR="127.0.0.1",
            HTTP_USER_AGENT='my_clever_agent',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.engine = import_module(settings.SESSION_ENGINE)
        self.store = self.engine.SessionStore()
        self.store.save()
        self.request_post.session = self.store
        self.request_post.user = AnonymousUser()
        self.request_get.session = self.store
        self.request_get.user = AnonymousUser()


class UpdateHitCountTests(HitCountTestBase):

    def test_anonymous_user_hit(self):
        """
        Test AnonymousUser Hit
        """
        response = HitCountMixin.hit_count(self.request_post, self.hit_count)

        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: session key')

    def test_anonymous_user_hit_not_counted(self):
        """
        Test Multiple AnonymousUser Hit, not counted
        """

        response = HitCountMixin.hit_count(self.request_post, self.hit_count)
        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: session key')

        response = HitCountMixin.hit_count(self.request_post, self.hit_count)
        self.assertFalse(response.hit_counted)
        self.assertEqual(response.hit_message, 'Not counted: session key has active hit')

    def test_anonymous_user_hit_counted_after_filter_active(self):
        """
        Test Multiple AnonymousUser Hit, counted because of filter active
        """
        # create a Hit ten days ago
        created = timezone.now() - timedelta(days=10)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = created

            response = HitCountMixin.hit_count(self.request_post, self.hit_count)

        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: session key')

        # test a Hit today, within the filter time
        response = HitCountMixin.hit_count(self.request_post, self.hit_count)
        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: session key')

    def test_registered_user_hit(self):
        """
        Test AnonymousUser Hit
        """
        self.request_post.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        response = HitCountMixin.hit_count(self.request_post, self.hit_count)

        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: user authentication')

    def test_registered_user_hit_not_counted(self):
        """
        Test Multiple AnonymousUser Hit, not counted
        """
        self.request_post.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        response = HitCountMixin.hit_count(self.request_post, self.hit_count)
        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: user authentication')

        response = HitCountMixin.hit_count(self.request_post, self.hit_count)
        self.assertFalse(response.hit_counted)
        self.assertEqual(response.hit_message, 'Not counted: authenticated user has active hit')

    def test_registered_user_hit_counted_after_filter_active(self):
        """
        Test Multiple AnonymousUser Hit, counted because of filter active
        """
        self.request_post.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        # create a Hit ten days ago
        created = timezone.now() - timedelta(days=10)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = created

            response = HitCountMixin.hit_count(self.request_post, self.hit_count)

        self.assertTrue(response.hit_counted)
        self.assertEqual(response.hit_message, 'Hit counted: user authentication')

        # test a Hit today, within the filter time
        response = HitCountMixin.hit_count(self.request_post, self.hit_count)
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
            self.request_post.session = store
            responses.append(HitCountMixin.hit_count(self.request_post, self.hit_count))

        self.assertTrue(responses[0].hit_counted)
        self.assertEqual(responses[0].hit_message, 'Hit counted: session key')
        self.assertTrue(responses[1].hit_counted)
        self.assertEqual(responses[1].hit_message, 'Hit counted: session key')
        self.assertFalse(responses[2].hit_counted)
        self.assertEqual(responses[2].hit_message, 'Not counted: hits per IP address limit reached')
        hit_count = HitCount.objects.get(pk=self.hit_count.pk)
        self.assertEqual(hit_count.hits, 2)

    @override_settings(HITCOUNT_EXCLUDE_USER_GROUP=('Admin',))
    def test_exclude_user_group(self):
        """
        Exclude user by adding a group setting.
        """
        self.request_post.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        group = Group.objects.create(name='Admin')
        group.user_set.add(self.request_post.user)

        response = HitCountMixin.hit_count(self.request_post, self.hit_count)
        self.assertFalse(response.hit_counted)
        self.assertEqual(response.hit_message, 'Not counted: user excluded by group')

    def test_blacklist_ip(self):
        """
        Test black listed IPs.
        """
        BlacklistIP.objects.create(ip="127.0.0.1")

        response = HitCountMixin.hit_count(self.request_post, self.hit_count)
        self.assertFalse(response.hit_counted)
        self.assertEqual(response.hit_message, 'Not counted: user IP has been blacklisted')

    def test_blacklist_user_agent(self):
        """
        Test black listed user agents.
        """
        BlacklistUserAgent.objects.create(user_agent="my_clever_agent")

        response = HitCountMixin.hit_count(self.request_post, self.hit_count)
        self.assertFalse(response.hit_counted)
        self.assertEqual(response.hit_message, 'Not counted: user agent has been blacklisted')


class UpdateHitCountJSONTests(HitCountTestBase):

    def test_require_ajax(self):
        """
        Test require ajax request or raise 404
        """
        non_ajax_request = self.factory.get('/')
        with self.assertRaises(Http404):
            HitCountJSONView.as_view()(non_ajax_request)

    def test_require_post_only(self):
        """
        Test require POST request or raise 404
        """
        non_ajax_request = self.factory.get('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        non_ajax_request.session = self.store
        response = HitCountJSONView.as_view()(non_ajax_request)
        json_response = json.loads(response.content.decode())
        json_expects = json.loads('{"error_message": "Hits counted via POST only.", "success": false}')
        self.assertEqual(json_response, json_expects)

    def test_count_hit(self):
        """
        Test a valid request.
        """
        response = HitCountJSONView.as_view()(self.request_post)
        self.assertEqual(response.content, b'{"hit_counted": true, "hit_message": "Hit counted: session key"}')

    def test_count_hit_invalid_hitcount_pk(self):
        """
        Test a valid request with an invalid hitcount pk.
        """
        wrong_pk_request = self.factory.post(
            '/', {'hitcountPK': 15},
            REMOTE_ADDR="127.0.0.1",
            HTTP_USER_AGENT='my_clever_agent',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        wrong_pk_request.session = self.store
        response = HitCountJSONView.as_view()(wrong_pk_request)
        self.assertEqual(response.content, b'HitCount object_pk not working')


class UpdateHitCountView(HitCountTestBase):

    def test_count_hit(self):
        """
        Test a valid request.
        """
        view = HitCountDetailView.as_view(model=Post)
        response = view(self.request_get, pk=self.post.pk)
        self.assertEqual(response.context_data['hitcount']['pk'], self.hit_count.pk)
        self.assertEqual(response.context_data['hitcount']['total_hits'], 0)

    def test_count_hit_incremented(self):
        """
        Increment a hit and then get the response.
        """
        view = HitCountDetailView.as_view(model=Post, count_hit=True)
        response = view(self.request_get, pk=self.post.pk)
        self.assertEqual(response.context_data['hitcount']['total_hits'], 1)
        self.assertEqual(response.context_data['hitcount']['pk'], self.hit_count.pk)

    def test_count_hit_incremented_only_once(self):
        """
        Increment a hit and then get the response.
        """
        view = HitCountDetailView.as_view(model=Post, count_hit=True)
        response = view(self.request_get, pk=self.post.pk)
        self.assertEqual(response.context_data['hitcount']['total_hits'], 1)
        self.assertEqual(response.context_data['hitcount']['pk'], self.hit_count.pk)
        view = HitCountDetailView.as_view(model=Post, count_hit=True)
        response = view(self.request_get, pk=self.post.pk)
        self.assertEqual(response.context_data['hitcount']['total_hits'], 1)
        self.assertEqual(response.context_data['hitcount']['pk'], self.hit_count.pk)


class TestDeprecationWarning(HitCountTestBase):
    """
    Remove these tests when functions are removed in 1.3
    """

    def test_json_warning(self):
        with warnings.catch_warnings(record=True) as w:
            update_hit_count_ajax(self.request_post, self.hit_count)
            self.assertTrue(issubclass(w[-1].category, RemovedInHitCount13Warning))

    def test_get_hit_count_warning(self):
        with warnings.catch_warnings(record=True) as w:
            _update_hit_count(self.request_post, self.hit_count)
            self.assertTrue(issubclass(w[-1].category, RemovedInHitCount13Warning))
