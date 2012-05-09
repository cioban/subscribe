# -*- encoding: utf-8 -*-
#############################################
# Sergio Cioban Filho - 10/07/2011 12:42:44 AM
#############################################

from django.forms import ModelForm, ModelChoiceField
from models import UserProfile
from django.forms import DateField, DateInput, CharField, ChoiceField
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.localflavor.br.forms import BRCPFField, BRPhoneNumberField, BRZipCodeField, BRStateSelect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from church.models import district


class UserCreationFormExtended(UserCreationForm):
	person_date		= DateField(label=u"Data de nascimento", widget=SelectDateWidget(years=range(1960, 2011)))
	person_cpf		= BRCPFField(label=u'CPF',help_text=u"Formato: XXX.XXX.XXX")
	person_phone	= BRPhoneNumberField(label=u'Telefone', help_text=u'Formato: XX-XXXX-XXXX')
	person_state	= CharField(label = 'Estado', widget = BRStateSelect())
	id_district		= ModelChoiceField(queryset=district.objects.all(), label="Distrito")
	person_city		= CharField(max_length=255, label="Cidade")
	GENDER_CHOICES  = (('', '----'),('M', 'Masculino'), ('F', 'Feminino'),)
	person_gender   = ChoiceField(choices=GENDER_CHOICES, label="Sexo", required=True)

	def __init__(self, *args, **kwargs):
		super(UserCreationFormExtended, self).__init__(*args, **kwargs)
		self.fields['first_name'].required = True
		self.fields['first_name'].label = "Nome"
		self.fields['last_name'].required = True
		self.fields['last_name'].label = "Sobrenome"
		self.fields['email'].required = True
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')

	def clean_email(self):
		data = self.cleaned_data['email']
		if User.objects.filter(email=data).exists():
			raise ValidationError("email já esta cadastrado, por favor utilize outro")
		return data

	def clean_person_cpf(self):
		data = self.cleaned_data['person_cpf']
		if UserProfile.objects.filter(person_cpf=data).exists():
			raise ValidationError("CPF já cadastrado")
		return data
