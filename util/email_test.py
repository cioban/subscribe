#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#############################################
# Sergio Cioban Filho - 29/10/2011 08:38:03
#############################################

#from django.core.management import setup_environ
#from subscribe import settings

#setup_environ(settings)

import os, sys
from xml.etree import ElementTree as ET
import urllib, httplib
from django.http import HttpResponse


ROOTDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(ROOTDIR, "../"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


### DJANGO
from django.conf import settings
from event.models import event, event_subscribe
from django.contrib.auth.models import User
### END - DJANGO

if __name__ == "__main__":


	user = User.objects.get(username='cioban')
	subject = "TESTE DE EMAIL".encode('utf-8')
	#message = u"Ola, %s s%, isso eh um teste do sistema %s\n ".encode('utf-8') % ( user.first_name.encode('utf-8'), user.last_name.encode('utf-8'), settings.SYS_NAME.encode('utf-8'), )
	message = "Ola, isso eh um teste do sistema\n "

	user.email_user(subject, message, from_email=None)
