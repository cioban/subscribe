# -*- encoding: utf-8 -*-
#############################################
# Sergio Cioban Filho - 17/07/2011 04:39:02 PM
#############################################

from django.contrib import admin
from models import event, event_price, event_subscribe
from django.db.models import CharField

class eventAdmin(admin.ModelAdmin):
	pass

class event_priceAdmin(admin.ModelAdmin):
	pass

class event_subscribeAdmin(admin.ModelAdmin):
	search_fields = ('id_user__username', 'id_user__first_name', 'id_user__last_name', 'id_user__email', 'TransacaoID', 'id_event__event_name')

admin.site.register(event)
admin.site.register(event_price)
admin.site.register(event_subscribe, event_subscribeAdmin)
