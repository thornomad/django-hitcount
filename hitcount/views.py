# -*- coding: utf-8 -*-

import warnings
from collections import namedtuple

from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.views.generic import View, DetailView

from hitcount.utils import get_ip
from hitcount.models import Hit, HitCount, BlacklistIP, BlacklistUserAgent
from hitcount.utils import RemovedInHitCount13Warning


class HitCountMixin(object):
    """
    Mixin to evaluate a HttpRequest and a HitCount and determine whether or not
    the HitCount should be incremented and the Hit recorded.
    """

    @classmethod
    def hit_count(self, request, hitcount):
        """
        Called with a HttpRequest and HitCount object it will return a
        namedtuple:

        UpdateHitCountResponse(hit_counted=Boolean, hit_message='Message').

        `hit_counted` will be True if the hit was counted and False if it was
        not.  `'hit_message` will indicate by what means the Hit was either
        counted or ignored.
        """
        UpdateHitCountResponse = namedtuple(
            'UpdateHitCountResponse', 'hit_counted hit_message')

        # as of Django 1.8.4 empty sessions are not being saved
        # https://code.djangoproject.com/ticket/25489
        if request.session.session_key is None:
            request.session.save()

        user = request.user
        try:
            is_authenticated_user = user.is_authenticated()
        except:
            is_authenticated_user = user.is_authenticated
        session_key = request.session.session_key
        ip = get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        hits_per_ip_limit = getattr(settings, 'HITCOUNT_HITS_PER_IP_LIMIT', 0)
        exclude_user_group = getattr(settings, 'HITCOUNT_EXCLUDE_USER_GROUP', None)

        # first, check our request against the IP blacklist
        if BlacklistIP.objects.filter(ip__exact=ip):
            return UpdateHitCountResponse(
                False, 'Not counted: user IP has been blacklisted')

        # second, check our request against the user agent blacklist
        if BlacklistUserAgent.objects.filter(user_agent__exact=user_agent):
            return UpdateHitCountResponse(
                False, 'Not counted: user agent has been blacklisted')

        # third, see if we are excluding a specific user group or not
        if exclude_user_group and is_authenticated_user:
            if user.groups.filter(name__in=exclude_user_group):
                return UpdateHitCountResponse(
                    False, 'Not counted: user excluded by group')

        # eliminated first three possible exclusions, now on to checking our database of
        # active hits to see if we should count another one

        # start with a fresh active query set (HITCOUNT_KEEP_HIT_ACTIVE)
        qs = Hit.objects.filter_active()

        # check limit on hits from a unique ip address (HITCOUNT_HITS_PER_IP_LIMIT)
        if hits_per_ip_limit:
            if qs.filter(ip__exact=ip).count() >= hits_per_ip_limit:
                return UpdateHitCountResponse(
                    False, 'Not counted: hits per IP address limit reached')

        # create a generic Hit object with request data
        hit = Hit(session=session_key, hitcount=hitcount, ip=get_ip(request),
                  user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],)

        # first, use a user's authentication to see if they made an earlier hit
        if is_authenticated_user:
            if not qs.filter(user=user, hitcount=hitcount):
                hit.user = user  # associate this hit with a user
                hit.save()

                response = UpdateHitCountResponse(
                    True, 'Hit counted: user authentication')
            else:
                response = UpdateHitCountResponse(
                    False, 'Not counted: authenticated user has active hit')

        # if not authenticated, see if we have a repeat session
        else:
            if not qs.filter(session=session_key, hitcount=hitcount):
                hit.save()
                response = UpdateHitCountResponse(
                    True, 'Hit counted: session key')
            else:
                response = UpdateHitCountResponse(
                    False, 'Not counted: session key has active hit')

        return response


class HitCountJSONView(View, HitCountMixin):
    """
    JSON response view to handle HitCount POST.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404()
        return super(HitCountJSONView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        msg = "Hits counted via POST only."
        return JsonResponse({'success': False, 'error_message': msg})

    def post(self, request, *args, **kwargs):
        hitcount_pk = request.POST.get('hitcountPK')

        try:
            hitcount = HitCount.objects.get(pk=hitcount_pk)
        except:
            return HttpResponseBadRequest("HitCount object_pk not working")

        hit_count_response = self.hit_count(request, hitcount)
        return JsonResponse(hit_count_response._asdict())


class HitCountDetailView(DetailView, HitCountMixin):
    """
    HitCountDetailView provides an inherited DetailView that will inject the
    template context with a `hitcount` variable giving you the number of
    Hits for an object without using a template tag.

    Optionally, by setting `count_hit = True` you can also do the business of
    counting the Hit for this object (in lieu of using JavaScript).  It will
    then further inject the response from the attempt to count the Hit into
    the template context.
    """
    count_hit = False

    def get_context_data(self, **kwargs):
        context = super(HitCountDetailView, self).get_context_data(**kwargs)
        if self.object:
            hit_count = HitCount.objects.get_for_object(self.object)
            hits = hit_count.hits
            context['hitcount'] = {'pk': hit_count.pk}

            if self.count_hit:
                hit_count_response = self.hit_count(self.request, hit_count)
                if hit_count_response.hit_counted:
                    hits = hits + 1
                context['hitcount']['hit_counted'] = hit_count_response.hit_counted
                context['hitcount']['hit_message'] = hit_count_response.hit_message

            context['hitcount']['total_hits'] = hits

        return context


def _update_hit_count(request, hitcount):
    """
    Deprecated in 1.2. Use hitcount.views.Hit CountMixin.hit_count() instead.
    """
    warnings.warn(
        "hitcount.views._update_hit_count is deprecated. "
        "Use hitcount.views.HitCountMixin.hit_count() instead.",
        RemovedInHitCount13Warning
    )
    return HitCountMixin.hit_count(request, hitcount)


def update_hit_count_ajax(request, *args, **kwargs):
    """
    Deprecated in 1.2. Use hitcount.views.HitCountJSONView instead.
    """
    warnings.warn(
        "hitcount.views.update_hit_count_ajax is deprecated. "
        "Use hitcount.views.HitCountJSONView instead.",
        RemovedInHitCount13Warning
    )
    view = HitCountJSONView.as_view()
    return view(request, *args, **kwargs)
