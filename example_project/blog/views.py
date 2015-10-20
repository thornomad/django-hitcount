# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView, TemplateView

from hitcount.views import HitCountDetailView

from blog.models import Post


class PostMixinDetailView(object):
    """
    Mixin to same us some typing.  Adds context for us!
    """
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostMixinDetailView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()[:5]
        context['post_views'] = ["ajax", "detail", "detail-with-count"]
        return context


class IndexView(PostMixinDetailView, TemplateView):
    template_name = 'blog/index.html'


class PostDetailJSONView(PostMixinDetailView, DetailView):
    template_name = 'blog/post_ajax.html'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PostDetailJSONView, cls).as_view(**initkwargs)
        return ensure_csrf_cookie(view)


class PostDetailView(PostMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view.
    """
    pass


class PostCountHitDetailView(PostMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view that will also perform the hitcount logic.
    """
    count_hit = True
