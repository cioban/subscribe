# coding=utf-8

from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from person.models import UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from models import event, event_price, event_subscribe, event_subscribe_intent
from forms import eventChoiceForm, pagStatusForm
from django.conf import settings
from pagamentolib import PagSeguro, LOG
from django.views.generic.simple import direct_to_template
from django.contrib.auth.models import User
from datetime import datetime
from random import randint
from django.db.models import Q

from pprint import pprint


def user_is_in_federation_group(user):
	if user:
		return user.groups.filter(name='federacao').count() == 1
	return False


@login_required
@user_passes_test(user_is_in_federation_group ,login_url='/')
def subscribe_list_identify(request):
	options = ['Aprovado', 'Completo']
	subscribes = event_subscribe.objects.filter(StatusTransacao__in=options).order_by('id_user__first_name')
	count = event_subscribe.objects.filter(StatusTransacao__in=options).count()

	return render_to_response("subscribe_list_identify.html", {'PAGE_NAME': 'Lista de inscritos', 'subscribes': subscribes, 'count': count }, context_instance=RequestContext(request))

@login_required
@user_passes_test(user_is_in_federation_group ,login_url='/')
def subscribe_list(request):
	if request.method == 'POST':
		form = pagStatusForm(request.POST)
	else:
		form = pagStatusForm()

	status = request.POST.get('StatusTransacao', 'todos')
	if status == 'todos':
		subscribes = event_subscribe.objects.all()
		count = event_subscribe.objects.all().count()
	elif status == 'aprovado_completo':
		options = ['Aprovado', 'Completo']

		#qs = Q(**{'StatusTransacao': 'Aprovado'})
		#qs |= Q(**{'StatusTransacao': 'Completo'})
		#subscribes = event_subscribe.objects.filter(qs)
		#count = event_subscribe.objects.filter(qs).count()

		subscribes = event_subscribe.objects.filter(StatusTransacao__in=options)
		count = event_subscribe.objects.filter(StatusTransacao__in=options).count()
	else:
		subscribes = event_subscribe.objects.filter(StatusTransacao = status)
		count = event_subscribe.objects.filter(StatusTransacao = status).count()

	return render_to_response("subscribe_list.html", {'form': form, 'PAGE_NAME': 'Lista de inscritos', 'subscribes': subscribes, 'count': count }, context_instance=RequestContext(request))


@login_required
def subscribe(request):
	if request.method == 'POST':
		form = eventChoiceForm(request.POST)
		if form.is_valid():
			step = request.GET['step']
			user_profile = request.user.userprofile

			if form.data['id_event'].isdigit() and form.data['id_event'] > 0:
				eventdata = event.objects.get(pk = form.data['id_event'])
				eventprice = event_price.objects.get(id_event = form.data['id_event'], id_district = user_profile.id_district )

			if (step.isdigit()) and (int(step) == 2) and eventprice:

				reference = user_profile.activation_key
				yet_subscribe = None
				try:
					yet_subscribe_check = event_subscribe.objects.filter(id_event = int(form.data['id_event']), id_user = request.user.id )
					for subscribed in yet_subscribe_check:
						yet_subscribe = subscribed
						if subscribed.StatusTransacao.encode('utf-8') == 'Cancelado' or subscribed.StatusTransacao == 'Cancelado':
							yet_subscribe = None
				except:
					yet_subscribe = None

				if yet_subscribe is not None:
					eventprice = str('%.2f' % (yet_subscribe.event_price,)).replace('.',',')
					response = render_to_response("subscribe.html", {'PAGE_NAME': 'Inscerver', 'eventdata': eventdata, 'eventprice': eventprice, 'pagseguro_email': settings.PAGSEGURO_EMAIL, 'reference': reference, 'event_subscribe': yet_subscribe, }, context_instance=RequestContext(request))


				else:
					user = request.user
					new_event = event.objects.get(pk = request.POST.get('id_event'))
					eventprice_pag = str(eventprice).replace(',','.')
					if request.POST['pay_choice'] == 'P':
						subscribe_intent = event_subscribe_intent(id_event=new_event, id_user=user, event_price=eventprice_pag)
						subscribe_intent.save()
						response = render_to_response("subscribe.html", {'PAGE_NAME': 'Inscerver', 'eventdata': eventdata, 'eventprice_pag': eventprice_pag, 'eventprice': eventprice, 'pagseguro_email': settings.PAGSEGURO_EMAIL, 'reference': reference }, context_instance=RequestContext(request))
					elif request.POST['pay_choice'] == 'F':
						response = render_to_response("subscribe.html", {'PAGE_NAME': 'Inscerver', 'eventdata': eventdata, 'eventprice_pag': eventprice_pag, 'eventprice': eventprice, 'reference': reference, 'pay_choice': request.POST['pay_choice'] }, context_instance=RequestContext(request))

			elif (step.isdigit()) and (int(step) == 3):
				log = LOG(True)
				LOG_TAG='[LOCAL] '
				log.write(LOG_TAG+"  === Nova inscricao LOCAL ===")
				log.write(LOG_TAG+"  ** CLIENT INFO: IP=["+str(request.META['REMOTE_ADDR'])+"] USER AGENT=["+str(request.META['HTTP_USER_AGENT'])+"] **")
				user = request.user
				new_event = event.objects.get(pk = request.POST.get('id_event'))

				price = request.POST.get('event_price').replace(',','.')
				new_date = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
				new_ID = randint(1,1000000000)
				new_subscribe = event_subscribe(TransacaoID=new_ID, DataTransacao=new_date, TipoPagamento='Federação depósito', StatusTransacao='Em Análise', event_price=price, subscribe_amount=request.POST.get('subscribe_amount'), id_event=new_event, id_user=user)

				INFO = 'TransacaoID=['+str(new_ID)+'] DataTransacao=['+str(new_date)+'] event_price=['+str(price)+'] id_event=['+str(new_event)+'] user='+str(user)
				log.write(LOG_TAG+"--INFO-- "+INFO)

				yet_subscribe = None
				try:
					yet_subscribe_check = event_subscribe.objects.filter(id_event=new_event, id_user=user)
					for subscribed in yet_subscribe_check:
						yet_subscribe = subscribed
						if subscribed.StatusTransacao.encode('utf-8') == 'Cancelado' or subscribed.StatusTransacao == 'Cancelado':
							yet_subscribe = None
							log.write(LOG_TAG+"    -> Existe uma inscricao CANCELADA cadastrada no BD...")
						else:
							if subscribed.DataTransacao != new_date:
								yet_subscribe = None

				except Exception, e:
					log.write(LOG_TAG+'Encontrado ERRO ao processar inscricao: '+str(e), level='ERROR')
					yet_subscribe = None

				if yet_subscribe is None:
					log.write(LOG_TAG+"    -> Salvando no BD")
					new_subscribe.save()

				return direct_to_template(request,'subscribe_finish.html')
			else:

				response = render_to_response("subscribe.html", {'form': form, 'PAGE_NAME': 'Inscerver' }, context_instance=RequestContext(request))


		else:
			response = render_to_response("subscribe.html", {'form': form, 'PAGE_NAME': 'Inscerver' }, context_instance=RequestContext(request))


	else:
		form = eventChoiceForm()
		response = render_to_response("subscribe.html", {'form': form, 'PAGE_NAME': 'Inscerver'}, context_instance=RequestContext(request))

	return response



@csrf_exempt
def pagreturn(request):
	"""
	Descricao:
	Armazena os dados do pedido e exibe a tela de pedido concluido.
	Verifica se o robo do PagSeguro enviou os dados do pedido via POST, e
	então armazena no banco de dados.
	Por fim, exibe a tela de pedido concluido com sucesso.
	"""
	log = LOG(True)
	log.write("  === Retorno do PAGSEGURO ===")
	log.write("  ** CLIENT INFO: IP=["+str(request.META['REMOTE_ADDR'])+"] USER AGENT=["+str(request.META['HTTP_USER_AGENT'])+"] **")


	if request.method == 'POST':
		log.write(" -> POST")
		log.write(" -> Encoding="+str(request.encoding))
		request.encoding = "ISO-8859-1"
		log.write(" -> Mudado="+request.encoding)

		try:
			# token gerado no painel de controle do PagSeguro
			token = settings.PAGSEGURO_TOKEN
			log.write("TOKEN="+str(token))

			p = PagSeguro()
			retorno = p.processar(token, request.POST)
			log.write("retorno="+str(retorno))

		except Exception, e:
			log.write('ERRO: '+str(e), level='ERROR')
			retorno = False

		if retorno == True:
			try:
				log.write(" === Cadastrando compra no BD ===")

				# Cadastra os dados recebidos no banco de dados.
				reference = request.POST.get('Referencia')
				log.write(" Referencia = "+reference)

				user_profile = get_object_or_404(UserProfile, activation_key=reference)
				user = User.objects.get(username = user_profile.user)
				log.write('username='+str(user))
				new_event = event.objects.get(pk = request.POST.get('ProdID_1'))
				log.write('event='+str(new_event))

				price = request.POST.get('ProdValor_1').replace(',','.')


				INFO = 'TransacaoID=['+str(request.POST.get('TransacaoID'))+'] DataTransacao=['+str(request.POST.get('DataTransacao'))+'] event_price=['+str(price)+'] id_event=['+str(new_event)+'] user='+str(user)
				log.write("--INFO-- "+INFO)

				yet_saved = None
				try:
					log.write("  => Pesquisando inscricoes no BD...")
					yet_subscribe_check = event_subscribe.objects.filter(id_event = new_event, id_user = user )
					for subscribed in yet_subscribe_check:
						yet_saved = subscribed
						log.write("  => Encontrada: "+str(subscribed))
						if subscribed.StatusTransacao.encode('utf-8') == 'Cancelado' or subscribed.StatusTransacao == 'Cancelado':
							yet_saved = None
							log.write("    -> Inscricao CANCELADA cadastrada no BD...")
						else:
							if subscribed.TransacaoID == request.POST.get('TransacaoID'):
								log.write("    -- Inscricao com o mesmo ID no BD. Nao vou salvar...")
								yet_saved = subscribed
								break
							if subscribed.DataTransacao == request.POST.get('DataTransacao'):
								log.write("    -- Inscricao com a mesma DATA no BD. Nao vou salvar...")
								yet_saved = subscribed
								break
				except Exception, e:
					log.write('Encontrado ERRO ao processar retorno: '+str(e), level='ERROR')
					yet_saved = None

				if yet_saved is not None:
					log.write(" -> Inscricao ja cadastrada no BD")
				else:
					new_subscribe = event_subscribe(TransacaoID=request.POST.get('TransacaoID'), DataTransacao=request.POST.get('DataTransacao'), TipoPagamento=request.POST.get('TipoPagamento'), StatusTransacao=request.POST.get('StatusTransacao'), event_price=price, subscribe_amount=request.POST.get('ProdQuantidade_1'), id_event=new_event, id_user=user)
					log.write(" -> Criou o objeto subscribe")
					new_subscribe.save()
					log.write(" -> Salvou no BD")
			except Exception, e:
				log.write('ERRO: '+str(e), level='ERROR')
				pass
			return HttpResponse('OK')
		else:
			return HttpResponse('FALHA')

	else:
		log.write(" -> Retorno final")
		# Carrega tela contendo a mensagem de compra realizada
		return direct_to_template(request,'subscribe_finish.html')



