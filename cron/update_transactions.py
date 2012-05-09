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

class LOG:
	def write(self, msg, type=None, level='INFO'):
		if self.logEnable is True:
			if ( type == "MARK" ):
				msg="------------------------------------------------------------"

			case = {
				'INFO': self.logger.info,
				'ERROR': self.logger.error,
				'WARNING': self.logger.warning
			}
			case[level](msg)

	def __init__(self, logEnable):
		if logEnable is True:
			import logging
			import logging.handlers
			#log_file = "/axs/traces/ipsecadm.trace"
			log_file = "/tmp/pagseguro.log"

			self.logger = logging.getLogger('pagseguro')
			hdlr = logging.handlers.RotatingFileHandler(filename=log_file, maxBytes=2097152, backupCount=10)
			formatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)s - %(message)s',"%d/%m/%Y %H:%M:%S")
			hdlr.setFormatter(formatter)
			self.logger.addHandler(hdlr)
			self.logger.setLevel(logging.INFO)

		self.logEnable = logEnable

class PagTransaction():

	def getTransactionXml(self, transactionId):
		conn = None
		conn = httplib.HTTPSConnection('ws.pagseguro.uol.com.br', timeout=30)
		GET_PATH="/v2/transactions/"+transactionId+'?email='+settings.PAGSEGURO_EMAIL+'&token='+settings.PAGSEGURO_TOKEN
		conn.request("GET", GET_PATH)
		response = conn.getresponse()
		conteudo = response.read()
		conn.close()

		return conteudo

#	def _enviar(self, params):
#		retorno = self._conectar(params)
#		self.log.write(" -> Retorno do POST para o PagSeguro: "+retorno)
#		if retorno == 'VERIFICADO':
#			return True
#		else:
#			return False


class xmlParser():
	def parse(self, xml_string):
		self.element = ET.XML(xml_string)


	def getTransactionStatus(self):
		status = None
		try:
			aux = self.element.find('status')
			if str(aux.text).isdigit():
				status = int(aux.text)
		except Exception:
			status = None
		return status

		#print element.get('reference')
		#for element_1 in element:
		#	print str(element_1.tag)+'='+str(element_1.text)
		#	for element_2 in element_1:
		#		print '	>>'+unicode(element_2.tag)+'='+unicode(element_2.text)
		#		for element_3 in element_2:
		#			print '		>>'+unicode(element_3.tag)+'='+unicode(element_3.text)


"""
1	Aguardando pagamento: o comprador iniciou a transação, mas até o momento o PagSeguro não recebeu nenhuma informação sobre o pagamento.
2	Em análise: o comprador optou por pagar com um cartão de crédito e o PagSeguro está analisando o risco da transação.
3	Paga: a transação foi paga pelo comprador e o PagSeguro já recebeu uma confirmação da instituição financeira responsável pelo processamento.
4	Disponível: a transação foi paga e chegou ao final de seu prazo de liberação sem ter sido retornada e sem que haja nenhuma disputa aberta.
5	Em disputa: o comprador, dentro do prazo de liberação da transação, abriu uma disputa.
6	Devolvida: o valor da transação foi devolvido para o comprador.
7	Cancelada: a transação foi cancelada sem ter sido finalizada.
"""


statusPag = {
	1: 'Aguardando Pagto',
	2: 'Em Análise',
	3: 'Completo',
	4: 'Completo',
	5: 'Cancelado',
	6: 'Cancelado',
	7: 'Cancelado',
}



if __name__ == "__main__":

	log = LOG(True)
	subscribes = event_subscribe.objects.all()
	for transaction in subscribes:
		try:
			ID = transaction.TransacaoID
			transaction_status_local = transaction.StatusTransacao.encode('utf-8')
			if (transaction_status_local == 'Cancelado'):
				continue

			if len(ID) >= 30:
				pagtransaction = PagTransaction()
				sendTransactionId = ID[:8]+'-'+ID[8:12]+'-'+ID[12:16]+'-'+ID[16:20]+'-'+ID[20:]
				XML = pagtransaction.getTransactionXml(sendTransactionId)
				xmlparser = xmlParser()
				xmlparser.parse(XML)
				status = xmlparser.getTransactionStatus()
				user = transaction.id_user
				transaction_status_remote = statusPag[status].encode('utf-8')
				price = str('%.2f' % (transaction.event_price,)).replace('.',',')

				subject = u"Alteração de staus de pagamento".encode('utf-8')
				message = u"Olá, %s %s,\nO sistema %s informa alteração no seu pagamento.\n\nConfira os dados abaixo.\n - Encontro: %s\n - Valor pago: R$ %s\n - Código: %s\n - Status anterior do pagamento: %s\n - NOVO STATUS DO PAGAMENTO: %s\n\nO status do seu pagamento pode ser verificado a qualquer momento acessando o sistema: %s\n\nCaso o NOVO STATUS DO PAGAMENTO seja 'Completo', você já está inscrito no encontro, bastando informar o código ou o seu CPF no momento da inscrição no dia do encontro.\n\nCaso o NOVO STATUS DO PAGAMENTO seja 'Cancelado', você deve acessar o sistema e se inscrever novamente através do LINK: %s\n OBS.: Toda a parte de pagamentos é controlada pelo PagSeguro, verifique com o PagSeguro o motivo do cancelamento do seu pagamento.\n\nEm caso de dúvidas entre em contato conosco através do email: federacaodejovens@gmail.com\n\n\nObrigado,\n Federação de Jovens\n Sexta Região".encode('utf-8') % ( user.first_name.encode('utf-8'), user.last_name.encode('utf-8'), settings.SYS_NAME.encode('utf-8'),
										str(transaction.id_event), price, str(ID), transaction_status_local, transaction_status_remote, settings.SYS_URL,
										settings.SYS_URL, )

				if (transaction_status_local == transaction_status_remote):
					continue
				else:
					log.write('A inscricao de: '+str(user)+' alterou de ['+transaction_status_local+'] para ['+transaction_status_remote+'] - event['+str(transaction.id_event.id_event)+']')
					transaction.StatusTransacao = transaction_status_remote
					#user.email_user(subject, message, from_email=None)
					transaction.save()

		except Exception, e:
			log.write(' -> Erro ao alterar trasacao: '+str(user)+' - '+' - '+statusPag[status]+' - '+transaction.StatusTransacao+' - event['+str(transaction.id_event.id_event)+']: '+str(e), level='ERROR')
			continue
