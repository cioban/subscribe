#!/usr/bin/env python
# -*- encoding: iso-8859-1 -*-
#############################################
# Sergio Cioban Filho - 29/10/2011 08:38:03
#############################################

import os, sys

ROOTDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(ROOTDIR, "../"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

### DJANGO
from django.conf import settings
#from event.models import event, event_subscribe
from person.models import UserProfile
from django.contrib.auth.models import User
### END - DJANGO


if __name__ == "__main__":

	lista = open('lista.csv', 'wb')
	profiles = UserProfile.objects.all()
	header = "NOME, EMAIL, DATA_NASCIMENTO, CIDADE, ESTADO, DISTRITO\n"
	lista.write(header)
	for profile in profiles:
		user = profile.user
		#print user
		#print type(user)
		#user = User.objects.get(username = user_profile.user)
		#DATA = u"%s %s, %s, %s, %s, %s, %s\n" % (
		DATA = "%s %s, %s, %s, %s, %s, %s\n" % (
				profile.user.first_name, profile.user.last_name,
				profile.user.email, profile.person_date.strftime("%d/%m/%Y"), profile.person_city,
				profile.person_state,
				profile.id_district,
				)

		lista.write(DATA.encode('iso-8859-1'))
		#print DATA


	lista.flush()
	lista.close()
