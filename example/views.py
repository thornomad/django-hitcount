from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

def home(request):
	"""
	homepage
	"""
	user = User.objects.all()[0]
	return render_to_response("home.html", {
		'user': user
	}, context_instance=RequestContext(request))
