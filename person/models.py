# -*- encoding: utf-8 -*-

from django.db import models

from django.contrib.localflavor.br.forms import BRCPFField, BRPhoneNumberField, BRStateSelect
from django.forms import DateField, DateInput
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user			= models.OneToOneField(User, unique=True)
	activation_key	= models.CharField(max_length=40, null=True)
	key_expires		= models.DateTimeField(null=True)
	id_district		= models.ForeignKey('church.district', db_column='id_district', verbose_name="Distrito")
	GENDER_CHOICES	= (('M', 'Masculino'), ('F', 'Feminino'),)
	person_gender	= models.CharField(max_length=1, choices=GENDER_CHOICES)
	person_date		= models.DateField(verbose_name="Data de nascimento",help_text="Formato: DD/MM/AAAA")
	person_cpf		= models.CharField(verbose_name=u'CPF', max_length=14, help_text=u'Informe o CPF. Formato: XXX.XXX.XXX-XX',unique=True)
	person_phone	= models.CharField(verbose_name=u'Telefone', max_length=12, help_text=u'Telefone para contato.Formato: XX-XXXX-XXXX')
	person_city		= models.CharField(max_length=255, verbose_name="Cidade")
	person_state	= models.CharField(verbose_name=u'Estado',max_length=2)


	class Meta:
		verbose_name = "Pessoa"
		verbose_name_plural = "Pessoas"

