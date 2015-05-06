from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from blog.models import Post

def index(request):
    post_list = Post.objects.all()[:5]
    template = loader.get_template('blog/index.html')
    context = RequestContext(request, {
        'post_list': post_list,
    })
    return HttpResponse(template.render(context))


@ensure_csrf_cookie #this is required for views that use django-hitcount
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_list = Post.objects.all()[:5]
    return render(request, 'blog/post.html',
        {'post' : post, 'post_list': post_list })
