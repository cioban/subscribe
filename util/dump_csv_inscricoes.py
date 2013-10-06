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
	lista = open('lista_inscricoes.csv', 'wb')
	subscribes = event_subscribe.objects.all()
	header = "TransacaoID, DataTransacao, TipoPagamento, StatusTransacao, VALOR, NOME, EMAIL, CPF,DATA_NASCIMENTO, CIDADE, ESTADO, DISTRITO\n"
	lista.write(header)
	for subscribe in subscribes:
		user = subscribe.id_user
		profile = user.userprofile

		DATA = "%s, %s, %s, %s, %s, %s %s, %s, %s, %s, %s, %s, %s\n" % (
				subscribe.TransacaoID, subscribe.DataTransacao, subscribe.TipoPagamento,
				subscribe.StatusTransacao, subscribe.event_price,
				user.first_name, user.last_name,
				user.email, profile.person_cpf, profile.person_date.strftime("%d/%m/%Y"), profile.person_city,
				profile.person_state,
				profile.id_district,
				)

		lista.write(DATA.encode('iso-8859-1'))
		#print DATA.encode('iso-8859-1')


	lista.flush()
	lista.close()
