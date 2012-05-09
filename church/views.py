# -*- enconding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import churchForm
from models import churchData, district

def new(request):
	if request.method == 'POST':
		form = churchForm(request.POST)
		if form.is_valid():
			form.save()
			response = render_to_response("save_ok.html", {})
			return response
	else:
		form = churchForm()

	response = render_to_response("church_new.html", {'form': form}, context_instance=RequestContext(request))
	return response


def districtsInfo(request):
	districts = district.objects.all()
	response = render_to_response("registration/districtsinfo.html", {'districts': districts}, context_instance=RequestContext(request))
	return response
