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

if len(sys.argv) != 2:
    print " -- Informe o nome do arquivo..."
    sys.exit()

nome_arquivo=sys.argv[1]

arquivo = open(nome_arquivo, 'r')

lista = arquivo.readlines()
lista.pop(0)
"""Transacao_ID    Cliente_Nome    Cliente_Email   Debito_Credito  Tipo_Transacao  Status  Tipo_Pagamento  Valor_Bruto Valor_Desconto  Valor_Taxa  Valor_Liquido   Transportadora  Num_Envio   Data_Transacao  Data_Compensacao    Ref_Transacao   Parcelas"""
"""
FEE3E233-F742-40D3-8266-E05FE27582E9    Jessé Carrapeiro
jee-drummer@hotmail.com Crédito Pagamento   Aprovada    Cartão de Crédito
150,0000    0,0000  10,0000 140,0000            23/10/2012 00:14:11 06/11/2012
00:18:46 3beda690b2c8e5ff26d8c10f5269cc29a6b958ac    3


E2D9FE75-3595-4A16-B217-78A09D14D448    ASSOCIAÇÃO DA IGREJA METODISTA DA 6A
REGIÃO financeiro@juventudemetodista.org.br    Débito  Saque   Aprovada
4.108,5900  0,0000  0,0000  4.108,5900          06/11/2012 21:40:23 06/11/2012
21:40:23     1

"""

total_bruto = 0
total_liquido = 0


for linha in lista:
    DATA = linha.split()

    if 'Saque' in DATA:
        continue

    #print DATA
    Transacao_ID = DATA[0].replace('-','')
    Parcelas = DATA.pop()
    Ref_Transacao = DATA.pop()
    Data_Compensacao = DATA.pop()+' '+DATA.pop()
    Data_Transacao = DATA.pop()+' '+DATA.pop()
    Valor_Liquido = float(DATA.pop().replace(',','.'))
    Valor_Taxa = float(DATA.pop().replace(',','.'))
    Valor_Desconto = float(DATA.pop().replace(',','.'))
    Valor_Bruto = float(DATA.pop().replace(',','.'))

    try:
        user = UserProfile.objects.get(activation_key=Ref_Transacao)
    except:
        if Valor_Bruto > 170:
            continue

    total_bruto += Valor_Bruto
    total_liquido += Valor_Liquido



print "=========="
print "TOTAL BRUTO: R$ "+str(total_bruto)
print "TOTAL LIQUIDO: R$ "+str(total_liquido)
print "=========="

arquivo.close()
sys.exit()
