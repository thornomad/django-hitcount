from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.utils import simplejson
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from hitcount.utils import get_ip
from hitcount.models import Hit, HitCount, BlacklistIP, BlacklistUserAgent

def _update_hit_count(request, hitcount):
    '''
    Evaluates a request's Hit and corresponding HitCount object and,
    after a bit of clever logic, either ignores the request or registers
    a new Hit.

    This is NOT a view!  But should be used within a view ...

    Returns True if the request was considered a Hit; returns False if not.
    '''
    user = request.user
    session_key = request.session.session_key
    ip = get_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
    hits_per_ip_limit = getattr(settings, 'HITCOUNT_HITS_PER_IP_LIMIT', 0)
    exclude_user_group = getattr(settings, 
                            'HITCOUNT_EXCLUDE_USER_GROUP', None)

    # first, check our request against the blacklists before continuing
    if BlacklistIP.objects.filter(ip__exact=ip) or \
            BlacklistUserAgent.objects.filter(user_agent__exact=user_agent):
        return False

    # second, see if we are excluding a specific user group or not
    if exclude_user_group and user.is_authenticated():
        if user.groups.filter(name__in=exclude_user_group):
            return False

    #start with a fresh active query set (HITCOUNT_KEEP_HIT_ACTIVE )
    qs = Hit.objects.filter_active() 

    # check limit on hits from a unique ip address (HITCOUNT_HITS_PER_IP_LIMIT)
    if hits_per_ip_limit:
        if qs.filter(ip__exact=ip).count() > hits_per_ip_limit:
            return False

    # create a generic Hit object with request data
    hit = Hit(  session=session_key,
                hitcount=hitcount,
                ip=get_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],)

    # first, use a user's authentication to see if they made an earlier hit
    if user.is_authenticated():
        if not qs.filter(user=user,hitcount=hitcount):
            hit.user = user #associate this hit with a user
            hit.save()
            return True

    # if not authenticated, see if we have a repeat session
    else:
        if not qs.filter(session=session_key,hitcount=hitcount):
            hit.save()

            # forces a save on this anonymous users session
            request.session.modified = True

            return True

    return False 

def json_error_response(error_message):
    return HttpResponse(simplejson.dumps(dict(success=False,
                                              error_message=error_message)))

# TODO better status responses - consider model after django-voting,
# right now the django handling isn't great.  should return the current
# hit count so we could update it via javascript (since each view will
# be one behind).
def update_hit_count_ajax(request):
    '''
    Ajax call that can be used to update a hit count.

    Ajax is not the only way to do this, but probably will cut down on 
    bots and spiders.

    See template tags for how to implement.
    '''

    # make sure this is an ajax request
    if not request.is_ajax():
        raise Http404()

    if request.method == "GET":
        return json_error_response("Hits counted via POST only.")

    hitcount_pk = request.POST.get('hitcount_pk')
    
    try:
        hitcount = HitCount.objects.get(pk=hitcount_pk)
    except:
        return HttpResponseBadRequest("HitCount object_pk not working")

    result = _update_hit_count(request, hitcount)

    if result:
        status = "success"
    else:
        status = "no hit recorded"

    json = simplejson.dumps({'status': status})
    return HttpResponse(json,mimetype="application/json")
