from django import template
from django.template import TemplateSyntaxError
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from hitcount.models import HitCount

register = template.Library()


def get_target_ctype_pk(context, object_expr):
    # I don't really understand how this is working, but I took it from the
    # comment app in django.contrib and the removed it from the Node.
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
        
        obj, created = HitCount.objects.get_or_create(content_type=ctype, 
                                            object_pk=object_pk)
        
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


class GetHitCountJavascript(template.Node):


    def handle_token(cls, parser, token):
        args = token.contents.split()
        
        if len(args) == 3 and args[1] == 'for':
            return cls(object_expr = parser.compile_filter(args[2]))

        else:
            raise TemplateSyntaxError, \
                    "'get_hit_count' requires " + \
                    "'for [object] in [timeframe] as [variable]' " + \
                    "(got %r)" % args

    handle_token = classmethod(handle_token)


    def __init__(self, object_expr):
        self.object_expr = object_expr


    def render(self, context):
        ctype, object_pk = get_target_ctype_pk(context, self.object_expr)
        
        obj, created = HitCount.objects.get_or_create(content_type=ctype, 
                        object_pk=object_pk)

        js =    "$.post( '" + reverse('hitcount_update_ajax') + "',"   + \
                "\n\t{ hitcount_pk : '" + str(obj.pk) + "' },\n"         + \
                "\tfunction(data, status) {\n"                         + \
                "\t\tif (data.status == 'error') {\n"                  + \
                "\t\t\t// do something for error?\n"                   + \
                "\t\t}\n\t},\n\t'json');"

        return js

def get_hit_count_javascript(parser, token):
    '''
    Return javascript for an object (goes in the document's onload function)
    and requires jQuery.  NOTE: only works on a single object, not an object
    list.

    For example:

    <script src="/media/js/jquery-latest.js" type="text/javascript"></script>
    <script type="text/javascript"><!--
    $(document).ready(function() {
        {% get_hit_count_javascript for [object] %}
    });
    --></script> 
    '''
    return GetHitCountJavascript.handle_token(parser, token)

register.tag('get_hit_count_javascript', get_hit_count_javascript)

