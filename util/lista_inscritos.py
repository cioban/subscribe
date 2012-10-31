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
from event.models import event, event_subscribe
from person.models import UserProfile
from django.contrib.auth.models import User
### END - DJANGO


if __name__ == "__main__":
	subscribes = event_subscribe.objects.filter(id_event = 1, id_user = 2)
	#subscribes = event_subscribe.objects.all()
	for subscribe in subscribes:
		if subscribe.StatusTransacao.encode('utf-8') == 'Cancelado' or subscribe.StatusTransacao == 'Cancelado':
			print("    -> Existe uma inscricao CANCELADA cadastrada no BD...")
		user = subscribe.id_user
		profile = user.userprofile

		DATA = "%s, %s, %s, %s, %s, %s %s, %s, %s, %s, %s, %s\n" % (
				subscribe.TransacaoID, subscribe.DataTransacao, subscribe.TipoPagamento,
				subscribe.StatusTransacao, subscribe.event_price,
				user.first_name, user.last_name,
				user.email, profile.person_date.strftime("%d/%m/%Y"), profile.person_city,
				profile.person_state,
				profile.id_district,
				)

		#lista.write(DATA.encode('iso-8859-1'))
		print DATA.encode('iso-8859-1')


	#lista.flush()
	#lista.close()
