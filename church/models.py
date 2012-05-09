from django.db import models

class churchData(models.Model):
	id_church	= models.AutoField(max_length=11, primary_key=True)
	church_name	= models.CharField(max_length=255, verbose_name="Nome da Igreja")
	city		= models.CharField(max_length=255, verbose_name="Cidade")
	neigh		= models.CharField(max_length=255, verbose_name="Bairro")
	state		= models.CharField(max_length=2, verbose_name="Sigla do estado", help_text="Apenas 2 letras. Ex.: SC ou PR")


	def __unicode__(self):
		return self.church_name+' - '+self.neigh+' - '+self.city+'-'+self.state

	class Meta:
		db_table = 'church'

class district(models.Model):
	id_district		= models.AutoField(max_length=11, primary_key=True)
	district_name	= models.CharField(max_length=255, verbose_name="Nome do distrito")
	district_church	= models.TextField(verbose_name="Igrejas do distrito")


	def __unicode__(self):
		return self.district_name

	class Meta:
		#app_label = 'Dados Igreja'
		verbose_name = "Distrito"
		verbose_name_plural = "Distritos"
