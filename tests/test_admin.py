from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from django.core.exceptions import PermissionDenied
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import User
from hitcount.admin import HitAdmin, HitCountAdmin
from hitcount.models import Hit, BlacklistIP, BlacklistUserAgent
from hitcount.utils import get_hitcount_model
from blog.models import Post
HitCount = get_hitcount_model()


class HitCountAdminTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.admin = HitCountAdmin(HitCount, AdminSite())

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.factory))


class HitAdminTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.admin = HitAdmin(Hit, AdminSite())
        self.request = self.factory.get(reverse(
            'admin:hitcount_hit_changelist'))
        setattr(self.request, 'session', 'session')
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)
        post = Post.objects.create(title='my title', content='my text')
        hit_count = HitCount.objects.create(content_object=post)
        for x in range(10):
            Hit.objects.create(hitcount=hit_count, ip='127.0.0.%s' % x,
                user_agent='agent_%s' % x)

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.factory))

    def test_get_actions(self):
        actions = ['blacklist_ips', 'blacklist_user_agents',
            'blacklist_delete_ips', 'blacklist_delete_user_agents',
            'delete_queryset']
        self.assertEqual(actions, list(self.admin.get_actions(self.request)
            .keys()))

    def test_blacklist_ips_single(self):
        qs = Hit.objects.filter(ip='127.0.0.5')
        self.admin.blacklist_ips(self.request, qs)
        ip = BlacklistIP.objects.get(pk=1)
        self.assertEqual(ip.ip, '127.0.0.5')
        self.assertEqual(len(BlacklistIP.objects.all()), 1)

    def test_blacklist_ips_multiple(self):
        qs = Hit.objects.all()[:5]
        self.admin.blacklist_ips(self.request, qs)
        ips = BlacklistIP.objects.values_list('ip', flat=True)
        self.assertEqual(ips[4], '127.0.0.5')
        self.assertEqual(len(BlacklistIP.objects.all()), 5)

    def test_blacklist_ips_add_only_once(self):
        qs = Hit.objects.filter(ip='127.0.0.5')
        self.admin.blacklist_ips(self.request, qs)
        self.assertEqual(len(BlacklistIP.objects.all()), 1)
        qs = Hit.objects.filter(ip='127.0.0.5')
        self.admin.blacklist_ips(self.request, qs)
        self.assertEqual(len(BlacklistIP.objects.all()), 1)

    def test_blacklist_user_agents_single(self):
        qs = Hit.objects.filter(ip='127.0.0.5')
        self.admin.blacklist_user_agents(self.request, qs)
        ua = BlacklistUserAgent.objects.get(pk=1)
        self.assertEqual(ua.user_agent, 'agent_5')
        self.assertEqual(len(BlacklistUserAgent.objects.all()), 1)

    def test_blacklist_user_agents_multiple(self):
        qs = Hit.objects.all()[:5]
        self.admin.blacklist_user_agents(self.request, qs)
        uas = BlacklistUserAgent.objects.values_list('user_agent', flat=True)
        self.assertEqual(uas[2], 'agent_7')
        self.assertEqual(len(BlacklistUserAgent.objects.all()), 5)

    def test_blacklist_user_agents_add_only_once(self):
        qs = Hit.objects.filter(ip='127.0.0.5')
        self.admin.blacklist_user_agents(self.request, qs)
        self.assertEqual(len(BlacklistUserAgent.objects.all()), 1)
        qs = Hit.objects.filter(ip='127.0.0.5')
        self.admin.blacklist_user_agents(self.request, qs)
        self.assertEqual(len(BlacklistUserAgent.objects.all()), 1)

    def test_delete_queryset(self):
        my_admin = User.objects.create_superuser('myuser',
            'myemail@example.com', '1234')
        self.request.user = my_admin
        qs = Hit.objects.all()[:5]
        self.admin.delete_queryset(self.request, qs)
        hit_count = HitCount.objects.get(pk=1)
        self.assertEqual(len(Hit.objects.all()), 5)
        self.assertEqual(hit_count.hits, 5)

    def test_delete_queryset_single_item(self):
        my_admin = User.objects.create_superuser('myuser',
            'myemail@example.com', '1234')
        self.request.user = my_admin
        qs = Hit.objects.filter(ip='127.0.0.5')
        self.admin.delete_queryset(self.request, qs)
        hit_count = HitCount.objects.get(pk=1)
        self.assertEqual(len(Hit.objects.all()), 9)
        self.assertEqual(hit_count.hits, 9)

    def test_delete_queryset_permission_denied(self):
        my_admin = User.objects.create_user('myuser', 'myemail@example.com',
            '1234')
        self.request.user = my_admin
        qs = Hit.objects.all()[:5]
        with self.assertRaises(PermissionDenied):
            self.admin.delete_queryset(self.request, qs)

    def test_blacklist_and_delete_ips(self):
        my_admin = User.objects.create_superuser('myuser',
            'myemail@example.com', '1234')
        self.request.user = my_admin
        qs = Hit.objects.all()[:5]
        self.admin.blacklist_delete_ips(self.request, qs)
        hit_count = HitCount.objects.get(pk=1)
        self.assertEqual(len(Hit.objects.all()), 5)
        self.assertEqual(hit_count.hits, 5)
        self.assertEqual(len(BlacklistIP.objects.all()), 5)

    def test_blacklist_and_delete_user_agents(self):
        my_admin = User.objects.create_superuser('myuser',
            'myemail@example.com', '1234')
        self.request.user = my_admin
        qs = Hit.objects.all()[:5]
        self.admin.blacklist_delete_user_agents(self.request, qs)
        hit_count = HitCount.objects.get(pk=1)
        self.assertEqual(len(Hit.objects.all()), 5)
        self.assertEqual(hit_count.hits, 5)
        self.assertEqual(len(BlacklistUserAgent.objects.all()), 5)
