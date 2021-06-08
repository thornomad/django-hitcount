from __future__ import unicode_literals
from datetime import timedelta
try:
    import unittest.mock as mock
except ImportError:
    import mock
from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from django.utils import timezone
from hitcount.models import Hit
from hitcount.utils import get_hitcount_model
from blog.models import Post
HitCount = get_hitcount_model()


class TemplateTagGetHitCountTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.post = Post.objects.get(pk=1)
        hit_count = HitCount.objects.create(content_object=self.post)
        for x in range(10):
            created = timezone.now() - timedelta(minutes=x * 15)
            with mock.patch('django.utils.timezone.now') as mock_now:
                mock_now.return_value = created
                Hit.objects.create(hitcount=hit_count)

    def test_returns_0(self):
        self.assertEqual(len(HitCount.objects.all()), 1)
        post2 = Post.objects.create(title='second', content='post!')
        out = Template('{% load hitcount_tags %}{% get_hit_count for post %}'
            ).render(Context({'post': post2}))
        self.assertEqual(str(0), out)
        self.assertEqual(len(HitCount.objects.all()), 2)

    def test_returns_10(self):
        out = Template('{% load hitcount_tags %}{% get_hit_count for post %}'
            ).render(Context({'post': self.post}))
        self.assertEqual(str(10), out)

    def test_as_variable(self):
        out = Template(
            '{% load hitcount_tags %}{% get_hit_count for post as hits %}Total Hits: {{ hits }}'
            ).render(Context({'post': self.post}))
        self.assertEqual('Total Hits: 10', out)

    def test_within(self):
        out = Template(
            '{% load hitcount_tags %}{% get_hit_count for post within "hours=1" %}'
            ).render(Context({'post': self.post}))
        self.assertEqual(str(4), out)

    def test_within_multiple_time_args(self):
        out = Template(
            '{% load hitcount_tags %}{% get_hit_count for post within "hours=1,minutes=30" %}'
            ).render(Context({'post': self.post}))
        self.assertEqual(str(6), out)

    def test_within_multiple_time_args_without_quotes(self):
        out = Template(
            '{% load hitcount_tags %}{% get_hit_count for post within hours=1,minutes=30 %}'
            ).render(Context({'post': self.post}))
        self.assertEqual(str(6), out)

    def test_within_as_var(self):
        out = Template(
            '{% load hitcount_tags %}{% get_hit_count for post within "hours=1" as hits %}Total Hits in last hour: {{ hits }}'
            ).render(Context({'post': self.post}))
        self.assertEqual('Total Hits in last hour: 4', out)

    def test_within_multiple_time_args_as_var(self):
        out = Template(
            '{% load hitcount_tags %}{% get_hit_count for post within "hours=1,minutes=30" as hits %}Total Hits in last 1h 15m: {{ hits }}'
            ).render(Context({'post': self.post}))
        self.assertEqual('Total Hits in last 1h 15m: 6', out)

    def test_get_js_variables(self):
        out = Template(
            '{% load hitcount_tags %}{% get_hit_count_js_variables for post as hit_count_js %}pk: {{ hit_count_js.pk }} || url: {{ hit_count_js.ajax_url }} || hits: {{ hit_count_js.hits }}'
            ).render(Context({'post': self.post}))
        pk = self.post.hit_count.pk
        self.assertEqual('pk: %s || url: /hitcount/hit/ajax/ || hits: 10' %
            pk, out)

    def test_insert_js_variables(self):
        out = Template(
            '{% load hitcount_tags %}{% insert_hit_count_js_variables for post %}'
            ).render(Context({'post': self.post}))
        pk = self.post.hit_count.pk
        self.assertEqual(
            """<script type="text/javascript">
var hitcountJS = {hitcountPK : '%s',hitcountURL : '/hitcount/hit/ajax/'};
</script>"""
             % pk, out)

    def test_parsing_errors(self):
        render = lambda t, c: Template(t).render(Context(c))
        self.assertRaises(TemplateSyntaxError, render,
            '{% load hitcount_tags %}{% get_hit_count for post within "foo=1,bar=30" %}'
            , {'post': self.post})
        self.assertRaises(TemplateSyntaxError, render,
            '{% load hitcount_tags %}{% get_hit_count for post %}', {
            'post_doesnt_context': self.post})
        self.assertRaises(TemplateSyntaxError, render,
            '{% load hitcount_tags %}{% get_hit_count post %}', {'post':
            self.post})
        self.assertRaises(TemplateSyntaxError, render,
            '{% load hitcount_tags %}{% get_hit_count post %}', {'post':
            'bob the baker'})

    def test_parsing_errors_get_js_variables(self):
        render = lambda t, c: Template(t).render(Context(c))
        self.assertRaises(TemplateSyntaxError, render,
            '{% load hitcount_tags %}{% get_hit_count_js_variables as hit_count_js %}'
            , {'post_variable_wrong': self.post})
        self.assertRaises(TemplateSyntaxError, render,
            '{% load hitcount_tags %}{% get_hit_count_js_variables as hit_count_js %}'
            , {'post': self.post})
        self.assertRaises(TemplateSyntaxError, render,
            '{% load hitcount_tags %}{% get_hit_count_js_variables for post as hit_count_js %}'
            , {'post': 'bob the baker'})

    def test_parsing_errors_insert_js_variables(self):
        render = lambda t, c: Template(t).render(Context(c))
        self.assertRaises(TemplateSyntaxError, render,
            '{% load hitcount_tags %}{% insert_hit_count_js_variables post %}',
            {'post': self.post})
        self.assertRaises(TemplateSyntaxError, render,
            '{% load hitcount_tags %}{% insert_hit_count_js_variables for post %}'
            , {'post_doesnt_context': self.post})
        self.assertRaises(TemplateSyntaxError, render,
            '{% load hitcount_tags %}{% insert_hit_count_js_variables for post %}'
            , {'post': 'bob the baker'})
