# coding=utf-8

from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from forms import UserCreationFormExtended
from models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime, random, sha
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt
def register(request):
	#new_user = User.objects.get(username='cioban')
	#new_profile = UserProfile.objects.get(user=2)
	#subject = u'[%s] Confirmação de conta' % ( settings.SYS_NAME, )
	#message = u"Olá, %s %s, obrigado por criar uma conta no sistema Inscrição Metodista\
	#				\n\nVocê tem 48 horas para confirmar a sua conta, clicando no link abaixo.\
	#				\n\n%s/register/confirm/%s" % ( new_user.first_name, new_user.last_name, settings.SYS_URL, new_profile.activation_key, )
	#print subject+' - '+message

	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	if request.method == 'POST':
			form = UserCreationFormExtended(request.POST)
			if form.is_valid():
				#new_user = form.save()
				##new_user = User.objects.create_user(username=form['username'], email=form['email'], first_name=form['first_name'], last_name=form['last_name'], password=form['password1'])
				#print str(dir(form))+' =============='
				new_user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
				new_user.first_name = form.cleaned_data['first_name']
				new_user.last_name = form.cleaned_data['last_name']
				new_user.is_active = False
				new_user.save()

				# Build the activation key for their account
				salt = sha.new(str(random.random())).hexdigest()[:5]
				activation_key = sha.new(salt+new_user.username).hexdigest()
				key_expires = datetime.datetime.today() + datetime.timedelta(2)

				# Create and save their profile
				person_date_year	= request.POST['person_date_year']
				person_date_month	= request.POST['person_date_month']
				person_date_day		= request.POST['person_date_day']
				if person_date_year.isdigit() and person_date_month.isdigit() and person_date_day.isdigit():
					person_date = person_date_year+'-'+person_date_month+'-'+person_date_day
					new_profile = UserProfile(user=new_user, activation_key=activation_key, key_expires=key_expires, person_cpf=form.cleaned_data['person_cpf'], person_phone=form.cleaned_data['person_phone'], person_state=form.cleaned_data['person_state'], id_district=form.cleaned_data['id_district'], person_city=form.cleaned_data['person_city'], person_date=person_date, person_gender=form.cleaned_data['person_gender'])
					new_profile.save()

					# Send an email with the confirmation link
					subject = u'[%s] Confirmação de conta' % ( settings.SYS_NAME, )
					message = u"Olá, %s %s, obrigado por criar uma conta no sistema %s\
					\n\nVocê tem 48 horas para confirmar a sua conta clicando no link abaixo.\
					\n\n%s/register/confirm/%s" % ( new_user.first_name, new_user.last_name, settings.SYS_NAME, settings.SYS_URL, new_profile.activation_key, )
					new_user.email_user(subject, message, from_email=None)

					return render_to_response('registration/register.html', {'email_sent': True}, context_instance=RequestContext(request))
				else:
					new_user.delete()
					form = UserCreationFormExtended(request.POST)

	else:
		form = UserCreationFormExtended()

	return render_to_response("registration/register.html", {
		'form': form}, context_instance=RequestContext(request))



@csrf_exempt
def confirm(request, activation_key):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
		#return render_to_response('confirm.html', {'has_account': True})

	user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
	user_account = user_profile.user

	if user_account.is_active is True:
		return HttpResponseRedirect("/")

	if user_profile.key_expires < datetime.datetime.today():
		user = User.objects.get(username = user_profile.user)
		user.delete()
		form = UserCreationFormExtended()
		return render_to_response('registration/register.html', {'form': form ,'key_expired': True}, context_instance=RequestContext(request))

	user_account.is_active = True
	user_account.save()
	return render_to_response('registration/register.html', {'user_validated': True}, context_instance=RequestContext(request))


