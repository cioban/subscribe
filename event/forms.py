# -*- encoding: utf-8 -*-
#############################################
# Sergio Cioban Filho - 10/07/2011 03:28:24 PM
#############################################

from django.forms import Form, ModelChoiceField, ChoiceField, Select
from models import event, event_price


class eventChoiceForm(Form):
	id_event = ModelChoiceField(queryset=event.objects.all(), label="Encontro", required=True)
	PAY_CHOICES  = (('', '----'),('P', 'Via PagSeguro'), ('F', 'Depósito direto para a federação'),)
	pay_choice   = ChoiceField(choices=PAY_CHOICES, label="Forma de pagamento", required=True)


class pagStatusForm(Form):
	StatusTransacao_CHOICES  = (('todos', 'Todos'), ('aprovado_completo', 'Aprovado+Completo'), ('Completo', 'Completo'), ('Aguardando Pagto', 'Aguardando Pagamento'), ('Aprovado', 'Aprovado'), (u'Em Análise', u'Em Análise'), ('Cancelado', 'Cancelado'),)
	StatusTransacao = ChoiceField(choices=StatusTransacao_CHOICES, label="Estado do pagamento", required=False,
					widget=Select(attrs={'onchange': 'this.form.submit();'}))
