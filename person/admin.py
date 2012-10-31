# -*- encoding: utf-8 -*-
#############################################
# Sergio Cioban Filho - 17/07/2011 04:39:02 PM
#############################################

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import UserProfile
from models import UserProfile


admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
	model = UserProfile
	search_fields = ('person_cpf', 'activation_key')

class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]
	search_fields = ('userprofile__person_cpf', 'userprofile__activation_key', 'email', 'first_name', 'last_name')

admin.site.register(User, UserProfileAdmin)
