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

from pprint import pprint


StatusTransacao_counters  = { 'Completo': 0, 'Aguardando Pagto': 0, 'Aprovado': 0, 'Em Análise': 0, 'Cancelado':0 }
all_subscribes = {}

if __name__ == "__main__":
	#subscribes = event_subscribe.objects.filter(id_event = 1, id_user = 2)
	subscribes = event_subscribe.objects.filter(id_event = 1)
	#subscribes = event_subscribe.objects.all()

	for subscribe in subscribes:

		if subscribe.StatusTransacao.encode('utf-8') != 'Cancelado' or subscribe.StatusTransacao != 'Cancelado':
			user = subscribe.id_user
			profile = user.userprofile

			try:
				DATA = all_subscribes[user.username]
			except KeyError:
				DATA = {
					'count': 0,
					'subscribe_list': [],
					'user': user,
				}


			DATA['count'] = DATA['count'] + 1
			DATA['subscribe_list'].append(subscribe)

			all_subscribes[user.username] = DATA
		#else:



	#pprint(all_subscribes)

	print
	print "##################################################"
	print "# == LISTA DE DUPLICADOS =="
	for user, DATA in all_subscribes.iteritems():


		# COUNTER
		for subscribe in DATA['subscribe_list']:
			try:
				StatusTransacao_counters[subscribe.StatusTransacao.encode('utf-8')] += 1
			except KeyError:
				print "erro: "+subscribe.StatusTransacao



		# DUPLICADOS
		if DATA['count'] > 1:
			user = DATA['user']
			profile = user.userprofile
			print "  ==> %s %s" % (user.first_name, user.last_name,)

			last_id = ''
			for subscribe in DATA['subscribe_list']:
				price = str('%.2f' % (subscribe.event_price,)).replace('.',',')
				print "    ** TransacaoID=[%s] DataTransacao=[%s] TipoPagamento=[%s] StatusTransacao=[%s] event_price=[%s]" % (
					subscribe.TransacaoID, subscribe.DataTransacao, subscribe.TipoPagamento, subscribe.StatusTransacao, price, )
				if subscribe.TransacaoID == last_id:
					print "      !!!!! APAGAR !!!!! "
					#subscribe.delete()


				last_id = subscribe.TransacaoID


	print "##################################################"

	print
	print "##################################################"
	print " ==== TOTAL DE INSCRITOS: "+str(len(all_subscribes))
	for key, data in StatusTransacao_counters.iteritems():
		print "  => "+str(key)+": "+str(data)
	print "##################################################"
	print
