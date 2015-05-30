# -*- coding: utf-8 -*-

from datetime import timedelta

try:
    import unittest.mock as mock
except ImportError:
    import mock

from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from django.utils import timezone

from hitcount.models import Hit, HitCount

from .models import Post


class TemplateTagGetHitCountTests(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title='my title', content='my text')
        hit_count = HitCount.objects.create(content_object=self.post)

        for x in range(10):
            created = timezone.now() - timedelta(minutes=x * 15)
            with mock.patch('django.utils.timezone.now') as mock_now:
                mock_now.return_value = created

                Hit.objects.create(hitcount=hit_count)

    def test_wrong_number_of_args(self):
        """
        get_hit_count should have 2, 4, or 6 args
        """
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{% load hitcount_tags %}"
                "{% get_hit_count post %}"
            ).render(Context({
                "post": self.post
            }))

    def test_for_obj_var_that_does_not_exist(self):
        """
        get_hit_count should be passed a obj variable that exists
        in the Context.
        """
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{% load hitcount_tags %}"
                "{% get_hit_count for post %}"
            ).render(Context({
                "post_doesnt_context": self.post
            }))

    def test_for_obj_when_var_is_not_a_model(self):
        """
        get_hit_count should be passed a valid obj that is a model;
        if it isn't, it should fail gracefully.
        """
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{% load hitcount_tags %}"
                "{% get_hit_count for post_is_string %}"
            ).render(Context({
                "post_is_string": 'bob'
            }))

    def test_returns_0(self):
        """
        {% get_hit_count for post%}

        If no HitCount object exists, the template tag should return zero
        and have created an object for the next time.
        """
        # no HitCounts to start
        self.assertEqual(len(HitCount.objects.all()), 1)
        post2 = Post.objects.create(title='second', content='post!')

        out = Template(
            "{% load hitcount_tags %}"
            "{% get_hit_count for post %}"
        ).render(Context({
            "post": post2
        }))

        # zero hits, but now one object
        self.assertEqual(str(0), out)
        self.assertEqual(len(HitCount.objects.all()), 2)

    def test_returns_10(self):
        """
        {% get_hit_count for post%}

        Test tag with multiple hits.
        """
        out = Template(
            "{% load hitcount_tags %}"
            "{% get_hit_count for post %}"
        ).render(Context({
            "post": self.post
        }))

        self.assertEqual(str(10), out)

    def test_as_variable(self):
        """
        {% get_hit_count for post as hits %}

        Test tag with output as variable.
        """
        out = Template(
            "{% load hitcount_tags %}"
            "{% get_hit_count for post as hits %}"
            "Total Hits: {{ hits }}"
        ).render(Context({
            "post": self.post
        }))

        self.assertEqual("Total Hits: 10", out)

    def test_within(self):
        """
        {% get_hit_count for [object] within [ex: "hours=1"] %}

        Test tag with multiple hits.
        """
        out = Template(
            "{% load hitcount_tags %}"
            '{% get_hit_count for post within "hours=1" %}'
        ).render(Context({
            "post": self.post
        }))

        self.assertEqual(str(4), out)

    def test_within_multiple_time_args(self):
        """
        {% get_hit_count for [object] within [ex: "hours=1,minutes=30"] %}

        Test tag with multiple hits and multiple time args.
        """
        out = Template(
            "{% load hitcount_tags %}"
            '{% get_hit_count for post within "hours=1,minutes=30" %}'
        ).render(Context({
            "post": self.post
        }))

        self.assertEqual(str(6), out)

    def test_within_multiple_time_args_without_quotes(self):
        """
        {% get_hit_count for [object] within [ex: hours=1,minutes=30] %}

        Test tag with multiple hits and multiple time args without quotes.
        """
        out = Template(
            "{% load hitcount_tags %}"
            '{% get_hit_count for post within hours=1,minutes=30 %}'
        ).render(Context({
            "post": self.post
        }))

        self.assertEqual(str(6), out)

    def test_within_as_var(self):
        """
        {% get_hit_count for [object] within [ex: "hours=1"] as [var] %}

        Test tag with multiple hits, get as a variable.
        """
        out = Template(
            '{% load hitcount_tags %}'
            '{% get_hit_count for post within "hours=1" as hits %}'
            'Total Hits in last hour: {{ hits }}'
        ).render(Context({
            "post": self.post
        }))

        self.assertEqual('Total Hits in last hour: 4', out)

    def test_within_multiple_time_args_as_var(self):
        """
        {% get_hit_count for [object] within [ex: "hours=1,minutes=30"] as [var] %}

        Test tag with multiple hits and multiple time args as a variable.
        """
        out = Template(
            "{% load hitcount_tags %}"
            '{% get_hit_count for post within "hours=1,minutes=30" as hits %}'
            'Total Hits in last 1h 15m: {{ hits }}'
        ).render(Context({
            "post": self.post
        }))

        self.assertEqual("Total Hits in last 1h 15m: 6", out)

    def test_invlaid_delta_time_variable(self):
        """
        get_hit_count should raise an error when wrong syntax for time
        """
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{% load hitcount_tags %}"
                '{% get_hit_count for post within "foo=1,bar=30" %}'
            ).render(Context({
                "post": self.post
            }))

    def test_js_variables(self):
        """
        {% get_hit_count_js_variables for [object] as [var_name] %}

        Test retrieval of javascript variables.
        """
        out = Template(
            "{% load hitcount_tags %}"
            '{% get_hit_count_js_variables for post as hit_count_js %}'
            'pk: {{ hit_count_js.pk }} || '
            'url: {{ hit_count_js.ajax_url }} || '
            'hits: {{ hit_count_js.hits }}'
        ).render(Context({
            "post": self.post
        }))

        self.assertEqual('pk: 1 || url: /hitcount/hit/ajax/ || hits: 10', out)

    def test_js_variables_wrong_number_of_variables(self):
        """
        {% get_hit_count_js_variables for [object] as [var_name] %}

        Test for error raised when wrong number of variables passed.
        """
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{% load hitcount_tags %}"
                '{% get_hit_count_js_variables as hit_count_js %}'
                'pk: {{ hit_count_js.pk }} || '
                'url: {{ hit_count_js.ajax_url }}'
            ).render(Context({
                "post": self.post
            }))

    def test_js_variables_for_obj_var_that_does_not_exist(self):
        """
        {% get_hit_count_js_variables for [object] as [var_name] %}

        Test for error raised when variable object passed does not exist.
        """
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{% load hitcount_tags %}"
                '{% get_hit_count_js_variables for post as hit_count_js %}'
                'pk: {{ hit_count_js.pk }} || '
                'url: {{ hit_count_js.ajax_url }}'
            ).render(Context({
                "post_doesnt_context": self.post
            }))

    def test_insert_js_variables(self):
        """
        {% insert_hit_count_js_variables for [object] %}

        Test for writing of js variables directly onto the template.
        """
        out = Template(
            "{% load hitcount_tags %}"
            '{% insert_hit_count_js_variables for post %}'
        ).render(Context({
            "post": self.post
        }))

        self.assertEqual('<script type="text/javascript">\n'
            'var hitcountJS = {hitcountPK : \'1\',hitcountURL :'
            ' \'/hitcount/hit/ajax/\'};\n</script>', out)

    def test_insert_js_variables_wrong_number_of_variables(self):
        """
        {% insert_hit_count_js_variables for [object] %}

        Test for error raised when wrong number of variables passed.
        """
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{% load hitcount_tags %}"
                '{% insert_hit_count_js_variables post %}'
            ).render(Context({
                "post": self.post
            }))

    def test_insert_js_variables_for_obj_var_that_does_not_exist(self):
        """
        {% insert_hit_count_js_variables for [object] %}

        Test for error raised when variable object passed does not exist.
        """
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{% load hitcount_tags %}"
                '{% insert_hit_count_js_variables for post %}'
            ).render(Context({
                "post_doesnt_context": self.post
            }))
