# -*- encoding: utf-8 -*-
#############################################
# Sergio Cioban Filho - 17/07/2011 04:39:02 PM
#############################################

from django.contrib import admin
from models import district

class districtAdmin(admin.ModelAdmin):
	search_fields = ('district_name', 'district_church')

admin.site.register(district, districtAdmin)
