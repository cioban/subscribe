# -*- encoding: utf-8 -*-
from django.db import models
from django.forms import DateField, DateInput
from django.contrib.auth.models import User


class event(models.Model):
	id_event		= models.AutoField(max_length=11, primary_key=True)
	event_name		= models.CharField(max_length=255, verbose_name="Nome")
	event_date_begin= models.DateField(verbose_name="Data de inicio do encontro",help_text="Formato: DD/MM/AAAA")
	event_date_end	= models.DateField(verbose_name="Data término do encontro",help_text="Formato: DD/MM/AAAA")
	event_city		= models.CharField(verbose_name=u'Cidade',max_length=255)
	event_state		= models.CharField(verbose_name=u'Estado',max_length=2)

	class Meta:
		db_table = 'event'
		verbose_name = "Encontro"
		verbose_name_plural = "Encontros"

	def __unicode__(self):
		return self.event_name+' - '+self.event_date_begin.strftime("%d/%m/%Y") +' a '+self.event_date_end.strftime("%d/%m/%Y")+' - '+self.event_city+'-'+self.event_state


class event_price(models.Model):
	id_event_price	= models.AutoField(max_length=11, primary_key=True)
	id_event		= models.ForeignKey(event)
	id_district		= models.ForeignKey('church.district', db_column='id_district', verbose_name="Distrito", null=True)
	price			= models.FloatField(verbose_name=u"Preço")

	def __unicode__(self):
		return str('%.2f' % (self.price,)).replace('.',',')

	class Meta:
		db_table = 'event_price'
		verbose_name = "Preco do encontro"
		verbose_name_plural = "Precos dos encontros"


"""
TipoPagamento:
-- PagSeguro --
  Pagamento: Pagamento PagSeguro
  Cartão de Crédito: Pagamento via cartão de crédito
  Oi Paggo: Pagamento via Oi Paggo
  Boleto: Pagamento via boleto bancário
  Pagamento Online: Pagamento via transferência online
-- Proprio --
  Federação depósito: Pagamento efetuado diretamente para a federação de Jovens via deposito bancario


StatusTransacao:
  Completo: Pagamento completo
  Aguardando Pagto: Aguardando pagamento do cliente
  Aprovado: Pagamento aprovado, aguardando compensação
  Em Análise: Pagamento aprovado, em análise pelo PagSeguro
  Cancelado: Pagamento cancelado pelo PagSeguro


"""


class event_subscribe(models.Model):
	StatusTransacao_CHOICES  = (('Completo', 'Completo'), ('Aguardando Pagto', 'Aguardando Pagamento'), ('Aprovado', 'Aprovado'), (u'Em Análise', u'Em Análise'), ('Cancelado', 'Cancelado'),)
	TipoPagamento_CHOICES  = (('Pagamento', 'Pagamento'), (u'Cartão de Crédito', u'Cartão de Crédito'), ('Oi Paggo', 'Oi Paggo'), ('Boleto', 'Boleto'), ('Pagamento Online', 'Pagamento Online'), (u'Federação depósito', u'Federação depósito'),)

	id_event_subscribe	= models.AutoField(max_length=11, primary_key=True)
	TransacaoID			= models.CharField(max_length=255, null=True)
	DataTransacao		= models.CharField(max_length=255, null=True)
	TipoPagamento		= models.CharField(max_length=30, null=True, choices=TipoPagamento_CHOICES)
	StatusTransacao		= models.CharField(max_length=30, null=True, choices=StatusTransacao_CHOICES)
	event_price			= models.FloatField(verbose_name=u"Preço")
	subscribe_amount	= models.IntegerField(default=1)
	id_event			= models.ForeignKey(event)
	id_user				= models.ForeignKey(User, db_column='id_user')





	class Meta:
		db_table = 'event_subscribe'
		verbose_name = "Inscricao"
		verbose_name_plural = "Inscricoes"

	def __unicode__(self):
		#return self.event_name+' - '+self.event_date_begin.strftime("%d/%m/%Y") +' a '+self.event_date_end.strftime("%d/%m/%Y")+' - '+self.event_city+'-'+self.event_state
		return self.id_user.first_name+' '+self.id_user.last_name+': '+self.id_event.event_name+' - '+self.id_event.event_date_begin.strftime("%d/%m/%Y")+' - R$ '+str('%.2f' % (self.event_price,)).replace('.',',')+' - '+self.TipoPagamento+' - '+self.StatusTransacao


#class event_subscribe_intent(models.Model):
#	id_event_subscribe_intent	= models.AutoField(max_length=11, primary_key=True)
#	id_event					= models.ForeignKey(event)
#	id_user						= models.ForeignKey(User, db_column='id_user')
#	TransacaoID					= models.CharField(max_length=255, null=True)
#	class Meta:
#		db_table = 'event_subscribe_intent'
