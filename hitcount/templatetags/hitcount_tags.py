# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import namedtuple

from django import template
from django.contrib.contenttypes.models import ContentType
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

from hitcount.models import HitCount

register = template.Library()


def get_hit_count_from_obj_variable(context, obj_variable, tag_name):
    """
    Helper function to return a HitCount for a given template object variable.

    Raises TemplateSyntaxError if the passed object variable cannot be parsed.
    """
    error_to_raise = template.TemplateSyntaxError(
        "'%(a)s' requires a valid individual model variable "
        "in the form of '%(a)s for [model_obj]'.\n"
        "Got: %(b)s" % {'a': tag_name, 'b': obj_variable}
    )

    try:
        obj = obj_variable.resolve(context)
    except template.VariableDoesNotExist:
        raise error_to_raise

    try:
        ctype = ContentType.objects.get_for_model(obj)
    except AttributeError:
        raise error_to_raise

    hit_count, created = HitCount.objects.get_or_create(
        content_type=ctype, object_pk=obj.pk)

    return hit_count


def return_period_from_string(arg):
    """
    Takes a string such as "days=1,seconds=30" and strips the quotes
    and returns a dictionary with the key/value pairs

    """
    period = {}

    if arg[0] == '"' and arg[-1] == '"':
        opt = arg[1:-1]  # remove quotes
    else:
        opt = arg

    for o in opt.split(","):
        key, value = o.split("=")
        period[str(key)] = int(value)

    return period


class GetHitCount(template.Node):

    def handle_token(cls, parser, token):
        args = token.contents.split()

        # {% get_hit_count for [obj] %}
        if len(args) == 3 and args[1] == 'for':
            return cls(obj_as_str=args[2])

        # {% get_hit_count for [obj] as [var] %}
        elif len(args) == 5 and args[1] == 'for' and args[3] == 'as':
            return cls(obj_as_str=args[2],
                       as_varname=args[4],)

        # {% get_hit_count for [obj] within ["days=1,minutes=30"] %}
        elif len(args) == 5 and args[1] == 'for' and args[3] == 'within':
            return cls(obj_as_str=args[2],
                       period=return_period_from_string(args[4]))

        # {% get_hit_count for [obj] within ["days=1,minutes=30"] as [var] %}
        elif len(args) == 7 and args[1] == 'for' and \
                args[3] == 'within' and args[5] == 'as':
            return cls(obj_as_str=args[2],
                       as_varname=args[6],
                       period=return_period_from_string(args[4]))

        else:  # TODO - should there be more troubleshooting prior to bailing?
            raise template.TemplateSyntaxError(
                "'get_hit_count' requires "
                "'for [object] in [period] as [var]' (got %r)" % args
            )

    handle_token = classmethod(handle_token)

    def __init__(self, obj_as_str, as_varname=None, period=None):
        self.obj_variable = template.Variable(obj_as_str)
        self.as_varname = as_varname
        self.period = period

    def render(self, context):
        hit_count = get_hit_count_from_obj_variable(context, self.obj_variable, 'get_hit_count')

        if self.period:  # if user sets a time period, use it
            try:
                hits = hit_count.hits_in_last(**self.period)
            except TypeError:
                raise template.TemplateSyntaxError(
                    "'get_hit_count for [obj] within [timedelta]' requires "
                    "a valid comma separated list of timedelta arguments. "
                    "For example, ['days=5,hours=6']. "
                    "Got these instead: %s" % self.period
                )
        else:
            hits = hit_count.hits

        if self.as_varname:  # if user gives us a variable to return
            context[self.as_varname] = str(hits)
            return ''
        else:
            return str(hits)


def get_hit_count(parser, token):
    """
    Returns hit counts for an object.

    - Return total hits for an object:
    {% get_hit_count for [object] %}

    - Get total hits for an object as a specified variable:
    {% get_hit_count for [object] as [var] %}

    - Get total hits for an object over a certain time period:
    {% get_hit_count for [object] within ["days=1,minutes=30"] %}

    - Get total hits for an object over a certain time period as a variable:
    {% get_hit_count for [object] within ["days=1,minutes=30"] as [var] %}

    The time arguments need to follow datetime.timedelta's limitations:
    Accepts days, seconds, microseconds, milliseconds, minutes,
    hours, and weeks.

    """
    return GetHitCount.handle_token(parser, token)

register.tag('get_hit_count', get_hit_count)


class WriteHitCountJavascriptVariables(template.Node):

    def handle_token(cls, parser, token):
        args = token.contents.split()

        if len(args) == 3 and args[1] == 'for':
            return cls(obj_variable=args[2])

        else:
            raise template.TemplateSyntaxError(
                'insert_hit_count_js_variables requires this syntax: '
                '"insert_hit_count_js_variables for [object]"\n'
                'Got: %s' % ' '.join(str(i) for i in args)
            )

    handle_token = classmethod(handle_token)

    def __init__(self, obj_variable):
        self.obj_variable = template.Variable(obj_variable)

    def render(self, context):
        hit_count = get_hit_count_from_obj_variable(context, self.obj_variable, 'insert_hit_count_js_variables')

        js = '<script type="text/javascript">\n' + \
            "var hitcountJS = {" + \
            "hitcountPK : '" + str(hit_count.pk) + "'," + \
            "hitcountURL : '" + str(reverse('hitcount:hit_ajax')) + "'};" + \
            "\n</script>"

        return js


def insert_hit_count_js_variables(parser, token):
    """
    Injects JavaScript global variables into your template.  These variables
    can be used in your JavaScript files to send the correctly mapped HitCount
    ID to the server (see: hitcount-jquery.js for an example).

    {% insert_hit_count_js_variables for [object] %}
    """
    return WriteHitCountJavascriptVariables.handle_token(parser, token)

register.tag('insert_hit_count_js_variables', insert_hit_count_js_variables)


class GetHitCountJavascriptVariables(template.Node):

    def handle_token(cls, parser, token):
        args = token.contents.split()

        if len(args) == 5 and args[1] == 'for' and args[3] == 'as':
            return cls(obj_variable=args[2], as_varname=args[4])

        else:
            raise template.TemplateSyntaxError(
                'get_hit_count_js_variables requires this syntax: '
                '"get_hit_count_js_variables for [object] as [var_name]."\n'
                'Got: %s' % ' '.join(str(i) for i in args)
            )

    handle_token = classmethod(handle_token)

    def __init__(self, obj_variable, as_varname):
        self.obj_variable = template.Variable(obj_variable)
        self.as_varname = as_varname

    def render(self, context):
        HitcountVariables = namedtuple('HitcountVariables', 'pk ajax_url hits')

        hit_count = get_hit_count_from_obj_variable(context, self.obj_variable, 'get_hit_count_js_variables')

        context[self.as_varname] = HitcountVariables(
            hit_count.pk, str(reverse('hitcount:hit_ajax')), str(hit_count.hits))

        return ''


def get_hit_count_js_variables(parser, token):
    """
    Injects JavaScript global variables into your template.  These variables
    can be used in your JavaScript files to send the correctly mapped HitCount
    ID to the server (see: hitcount-jquery.js for an example).

    {% get_hit_count_js_variables for [object] as [var_name] %}

    Will provide two variables:
        [var_name].pk = the hitcount pk to be sent via JavaScript
        [var_name].ajax_url = the relative url to post the ajax request to
    """
    return GetHitCountJavascriptVariables.handle_token(parser, token)

register.tag('get_hit_count_js_variables', get_hit_count_js_variables)


class WriteHitCountJavascript(template.Node):

    JS_TEMPLATE = """
<script type="text/javascript">
//<![CDATA[
jQuery(document).ready(function($) {
    $.postCSRF("%s", {
      hitcountPK: "%s"
    });
});
//]]>
</script>
"""

    JS_TEMPLATE_DEBUG = """
<script type="text/javascript">
//<![CDATA[
jQuery(document).ready(function($) {
    $.postCSRF("%s", {
      hitcountPK: "%s"
    }).done(function(data) {
      console.log('django-hitcount: AJAX POST succeeded.');
      console.log(data);
    }).fail(function(data) {
      console.log('django-hitcount: AJAX POST failed.');
      console.log(data);
    });
});
//]]>
</script>
"""

    def handle_token(cls, parser, token):
        args = token.contents.split()

        if len(args) == 3 and args[1] == 'for':
            return cls(obj_variable=args[2], debug=False)
        elif len(args) == 4 and args[1] == 'for' and args[3] == 'debug':
            return cls(obj_variable=args[2], debug=True)
        else:
            raise template.TemplateSyntaxError(
                'insert_hit_count_js requires this syntax: '
                '"insert_hit_count_js for [object]"\n'
                '"insert_hit_count_js for [object] debug"'
                'Got: %s' % ' '.join(str(i) for i in args)
            )

    handle_token = classmethod(handle_token)

    def __init__(self, obj_variable, debug):
        self.obj_variable = template.Variable(obj_variable)
        self.debug = debug

    def render(self, context):
        hit_count = get_hit_count_from_obj_variable(
            context,
            self.obj_variable,
            'insert_hit_count_js'
        )
        template = self.JS_TEMPLATE_DEBUG if self.debug else self.JS_TEMPLATE
        return template % (str(reverse('hitcount:hit_ajax')), str(hit_count.pk))


def insert_hit_count_js(parser, token):
    """
    Injects the JavaScript into your template that works with jquery.postcsrf.js.

    {% insert_hit_count_js_variables for [object] %}
    """
    return WriteHitCountJavascript.handle_token(parser, token)


register.tag('insert_hit_count_js', insert_hit_count_js)
