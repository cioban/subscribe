# -*- encoding: utf-8 -*-
#############################################
# Sergio Cioban Filho - 10/07/2011 03:28:24 PM
#############################################

from django.forms import ModelForm, CharField
from models import churchData
from django.contrib.localflavor.br.forms import BRPhoneNumberField, BRZipCodeField, BRStateSelect

class churchForm(ModelForm):
	state	= CharField(label = 'Estado', widget = BRStateSelect())
	class Meta:
		model = churchData
