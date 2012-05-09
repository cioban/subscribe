# -*- encoding: utf-8 -*-
#############################################
# Sergio Cioban Filho - 16/07/2011 11:27:37 AM
#############################################
from django.conf import settings
from django.utils.html import escape


def get_sys_tag(request):
	sys_tag = escape(settings.SYS_NAME+' - '+settings.SYS_VERSION)
	return { 'SYS_TAG': sys_tag }
