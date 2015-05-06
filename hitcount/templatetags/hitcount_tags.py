from collections import namedtuple

from django import template
from django.template import TemplateSyntaxError
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.exceptions import MultipleObjectsReturned

from hitcount.models import HitCount

register = template.Library()


def get_target_ctype_pk(context, object_expr):
    # I don't really understand how this is working, but I took it from the
    # comment app in django.contrib and then removed it from the Node.
    try:
        obj = object_expr.resolve(context)
    except template.VariableDoesNotExist:
        return None, None

    return ContentType.objects.get_for_model(obj), obj.pk


def return_period_from_string(arg):
    '''
    Takes a string such as "days=1,seconds=30" and strips the quotes
    and returns a dictionary with the key/value pairs
    '''
    period = {}

    if arg[0] == '"' and arg[-1] == '"':
        opt = arg[1:-1] #remove quotes
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
            return cls(object_expr = parser.compile_filter(args[2]))

        # {% get_hit_count for [obj] as [var] %}
        elif len(args) == 5 and args[1] == 'for' and args[3] == 'as':
            return cls(object_expr = parser.compile_filter(args[2]),
                        as_varname  = args[4],)

        # {% get_hit_count for [obj] within ["days=1,minutes=30"] %}
        elif len(args) == 5 and args[1] == 'for' and args[3] == 'within':
            return cls(object_expr = parser.compile_filter(args[2]),
                        period = return_period_from_string(args[4]))

        # {% get_hit_count for [obj] within ["days=1,minutes=30"] as [var] %}
        elif len(args) == 7 and args [1] == 'for' and \
                args[3] == 'within' and args[5] == 'as':
            return cls(object_expr = parser.compile_filter(args[2]),
                        as_varname  = args[6],
                        period      = return_period_from_string(args[4]))

        else: # TODO - should there be more troubleshooting prior to bailing?
            raise TemplateSyntaxError, \
                    "'get_hit_count' requires " + \
                    "'for [object] in [timeframe] as [variable]' " + \
                    "(got %r)" % args

    handle_token = classmethod(handle_token)


    def __init__(self, object_expr, as_varname=None, period=None):
        self.object_expr = object_expr
        self.as_varname = as_varname
        self.period = period


    def render(self, context):
        ctype, object_pk = get_target_ctype_pk(context, self.object_expr)

        try:
            obj, created = HitCount.objects.get_or_create(content_type=ctype, object_pk=object_pk)
        except MultipleObjectsReturned:
            # from hitcount.models
            # Because we are using a models.TextField() for `object_pk` to
            # allow *any* primary key type (integer or text), we
            # can't use `unique_together` or `unique=True` to guarantee
            # that only one HitCount object exists for a given object.

            # remove duplicate
            items = HitCount.objects.all().filter(content_type=ctype, object_pk=object_pk)
            obj = items[0]
            for extra_items in items[1:]:
                extra_items.delete()

        if self.period: # if user sets a time period, use it
            try:
                hits = obj.hits_in_last(**self.period)
            except:
                hits = '[hitcount error w/time period]'
        else:
            hits = obj.hits

        if self.as_varname: # if user gives us a variable to return
            context[self.as_varname] = str(hits)
            return ''
        else:
            return str(hits)


def get_hit_count(parser, token):
    '''
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
    '''
    return GetHitCount.handle_token(parser, token)

register.tag('get_hit_count', get_hit_count)

class WriteHitCountJavascriptVariables(template.Node):

    def handle_token(cls, parser, token):
        args = token.contents.split()

        if len(args) == 3 and args[1] == 'for':
            return cls(object_expr = parser.compile_filter(args[2]))

        else:
            raise TemplateSyntaxError, \
                    'insert_hit_count_js_variables requires this syntax: ' + \
                    '"insert_hit_count_js_variables for [object]"\n' + \
                    'got %r' % args

    handle_token = classmethod(handle_token)

    def __init__(self, object_expr):
        self.object_expr = object_expr

    def render(self, context):
        ctype, object_pk = get_target_ctype_pk(context, self.object_expr)

        obj, created = HitCount.objects.get_or_create(content_type=ctype, object_pk=object_pk)

        js =    '<script type="text/javascript">\n'   + \
                "var hitcountJS = {" + \
                "hitcountPK : '" + str(obj.pk) + "'," + \
                "hitcountURL : '"+ str(reverse('hitcount_update_ajax')) + "'};"         + \
                "\n</script>"

        return js


def insert_hit_count_js_variables(parser, token):
    '''
    Injects JavaScript global variables into your template.  These variables
    can be used in your JavaScript files to send the correctly mapped HitCount
    ID to the server (see: hitcount-jquery.js for an example).

    {% insert_hit_count_js_variables for [object] %}
    '''
    return WriteHitCountJavascriptVariables.handle_token(parser, token)

register.tag('insert_hit_count_js_variables', insert_hit_count_js_variables)

class GetHitCountJavascriptVariables(template.Node):

    def handle_token(cls, parser, token):
        args = token.contents.split()

        if len(args) == 5 and args[1] == 'for' and args[3] == 'as':
            return cls(object_expr = parser.compile_filter(args[2]), as_varname  = args[4])

        else:
            raise TemplateSyntaxError, \
                    'get_hit_count_js_variables requires this syntax: ' + \
                    '"get_hit_count_js_variables for [object] as [var_name]"\n' + \
                    'got %r' % args

    handle_token = classmethod(handle_token)

    def __init__(self, object_expr, as_varname):
        self.object_expr = object_expr
        self.as_varname = as_varname

    def render(self, context):
        HitcountVariables = namedtuple('HitcountVariables', 'pk ajax_url')
        ctype, object_pk = get_target_ctype_pk(context, self.object_expr)

        obj, created = HitCount.objects.get_or_create(content_type=ctype, object_pk=object_pk)

        context[self.as_varname] = HitcountVariables(obj.pk, str(reverse('hitcount_update_ajax')))

        return ''


def get_hit_count_js_variables(parser, token):
    '''
    Injects JavaScript global variables into your template.  These variables
    can be used in your JavaScript files to send the correctly mapped HitCount
    ID to the server (see: hitcount-jquery.js for an example).

    {% get_hit_count_js_variables for [object] as [var_name] %}

    Will provide two variables:
        [var_name].pk = the hitcount pk to be sent via JavaScript
        [var_name].ajax_url = the relative url to post the ajax request to
    '''
    return GetHitCountJavascriptVariables.handle_token(parser, token)

register.tag('get_hit_count_js_variables', get_hit_count_js_variables)


