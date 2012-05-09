from django.conf.urls.defaults import patterns, include, url
#from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'event.views.subscribe'),
	#url(r'^mydata/', 'person.views.list'),
	url(r'^districtsinfo/', 'church.views.districtsInfo'),
	url(r'^return/', 'event.views.pagreturn'),

	url(r'^subscribelist/', 'event.views.subscribe_list'),
	url(r'^subscribelistid/', 'event.views.subscribe_list_identify'),

	#url(r'^person/(?P<person_id>\d+)/$', 'person.views.detail'),
	#url(r'^person/new/', 'person.views.new'),
	#url(r'^church/new/', 'church.views.new'),
	#url(r'^event/', 'event.views.list'),



	url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',name="logout"),
	url(r'^register/confirm/(?P<activation_key>\S+)/$', 'person.views.confirm'),
	url(r'^register/$', 'person.views.register',name="register"),
	url(r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
	url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
	url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm'),
	url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
	url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
#print "OUTRO = "+str(staticfiles_urlpatterns())
