#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#############################################
# Sergio Cioban Filho - 30/09/2011 09:57:33
#############################################

import sys
import urllib2, urllib, httplib
from django.http import HttpResponse


class Pagamento(object):
	def __init__(self):
		self.log = LOG(True)

	def _conectar(self, params):
		conn = None
		conn = httplib.HTTPSConnection('pagseguro.uol.com.br', timeout=30)
		query_str = urllib.urlencode(params)
		http_header = {"Content-type": "application/x-www-form-urlencoded", 'charset': 'ISO-8859-1', "Accept": "text/plain"}
		conn.request("POST", "/pagseguro-ws/checkout/NPI.jhtml", query_str, http_header)
		response = conn.getresponse()
		conteudo = response.read()
		conn.close()

		return conteudo

	def _enviar(self, params):
		retorno = self._conectar(params)
		self.log.write(" -> Retorno do POST para o PagSeguro: "+retorno)
		if retorno == 'VERIFICADO':
			return True
		else:
			return False


class PagSeguro(Pagamento):
	def processar(self, token, params):
		log = LOG(True)
		log.write(" -> Processando o POST do PagSeguro")

		try:
			if not params:
				log.write(" -> Sem dados para envio", level='WARNING')
				return False
			else:
				log.write(" -> Adicionando token e comando")
				post_data = {}
				for key, value in params.items():
					post_data[key] = value.encode("iso-8859-1")

				post_data['Comando'] = 'validar'
				post_data['Token'] = token

				log.write(" -> Realizando POST...")
				return self._enviar(post_data)
		except Exception, e:
			log.write(" -> Problema ao enviar o POST para o PagSeguro: "+str(e), level='ERROR')
			return False

	def getStatus(self, tansactionId):
		conn = None
		conn = httplib.HTTPSConnection('pagseguro.uol.com.br', timeout=30)
		query_str = urllib.urlencode(params)
		http_header = {"Content-type": "application/x-www-form-urlencoded", 'charset': 'ISO-8859-1', "Accept": "text/plain"}
		conn.request("POST", "/pagseguro-ws/checkout/NPI.jhtml", query_str, http_header)
		response = conn.getresponse()
		conteudo = response.read()
		conn.close()
		#https://ws.pagseguro.uol.com.br/v2/transactions/3F0888D0-C97D-4CBA-8861-2CBF633B7C70?email=financeiro@juventudemetodista.org.br&token=2B80667665C9452483300B44A8AFA2D2


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


