from django.shortcuts import render, redirect

from resumen.models import Debate
from debate.models import Postura, Argumento, Valoracion, Respuesta, Edicion, Participantes, Visita
from perfil.models import Perfil, Notificacion
from debate.forms import newArgForm1,newArgForm0, newCounterargForm

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import *
import itertools
import json
import datetime
import pytz

##@brief Funcion que showDebate el debate
##@param request solicitud web
##@param id_debate id del debate solicitado por la url dinamica
##@return render redirecciona a "Debate" si el debate esta abierto y "debate_cerrado" si no
##@warning Login is required
@login_required
def showDebate(request, id_debate): #debate_id
	max_length = Debate.objects.get(id_debate=id_debate).largo
	creator=[('username', User.objects.get(id=request.user.id).username),
	         ('alias',Perfil.objects.get(user= request.user).alias)]
	arg_form0 = newArgForm0(creador=creator,max_length=max_length)
	arg_form1 = newArgForm1(creador=creator,max_length=max_length)
	counterarg_form = newCounterargForm(creador=creator,max_length=max_length)
	debate = Debate.objects.get(id_debate= id_debate)
	visits = visitCount(debate, request.user)
	if request.method == 'POST':
		#solicitud de valorar un argumento
		if 'id_arg' in request.POST:
			respuesta = rateArgument(request)
			return HttpResponse(respuesta)
		#solicitud de publicar un contraargumento a favor
		if 'counterargument0' in request.POST:
			counterarg = newCounterargument(request, id_debate, "id_argumento0")
			return redirect(showDebate,id_debate)
		#solicitud de publicar un contraargumento en contra
		if 'counterargument1' in request.POST:
			counterarg = newCounterargument(request, id_debate, "id_argumento1")
			return redirect(showDebate,id_debate)
		#solicitud de eliminar un argumento
		if 'id_arg_delete' in request.POST:
			id_debate = elimina_argumento(request)
			return redirect(showDebate,id_debate)

	owner_user_id = debate.id_usuario_id #usuario creador
	owner_user = User.objects.get(id= owner_user_id)
	counterarg_num = debate.num_rebate
	args_num = debate.num_argumento
	change_position_num = debate.num_cambio_postura
	counterarg_type = debate.tipo_rebate
	try:
		owner_profile = Perfil.objects.get(user= owner_user)
		owner_profile = owner_profile.alias
	except:
		owner_profile = 'username'

	usuario_actual_alias = Perfil.objects.get(user= request.user)
	actual_user_id = request.user.id

	infavor_arguments = Argumento.objects.filter(id_debate_id= id_debate, postura= 1)
	against_arguments = Argumento.objects.filter(id_debate_id= id_debate, postura= 0)
	infavor_args_list = argumentData(infavor_arguments, request.user.id, counterarg_num, id_debate)
	against_args_list = argumentData(against_arguments, request.user.id, counterarg_num, id_debate)
	against_args_list = sorted(against_args_list, key=lambda rate: rate['rate'], reverse=True)
	infavor_args_list = sorted(infavor_args_list, key=lambda rate: rate['rate'], reverse=True)

	actual_usr_args_num = Argumento.objects.filter(id_debate_id= id_debate, id_usuario_id=request.user ).count()
	if actual_usr_args_num < args_num:
		can_argue = True
	else:
		can_argue = False

	try:
		actual_user_position = Postura.objects.get(id_usuario_id= actual_user_id, id_debate_id=id_debate)
		position_exist = True
		change_position = actual_user_position.cuenta_cambios
	except:
		actual_user_position = "No definido"
		position_exist = False
		change_position = 0

	if change_position < change_position_num:
		can_change_position = True
	else:
		can_change_position = False
	counterarg_target = "Ambos"
	if position_exist:
		if actual_user_position.postura == 1:
			actual_user_position = "A Favor"
			if counterarg_type == 1:
				counterarg_target = "En Contra"
		else:
			actual_user_position = "En Contra"
			if counterarg_type == 1:
				counterarg_target = "A Favor"
	infavor_position=Postura.objects.filter(id_debate_id=id_debate, postura=1)
	against_position=Postura.objects.filter(id_debate_id=id_debate, postura=0)
	infavor_position_num=infavor_position.count()
	against_position_num=against_position.count()
	if (int(against_position_num+infavor_position_num)==0):
		against_percent=0
		infavor_percent=0
	else:
		infavor_percent = round(float(infavor_position_num) / float(against_position_num+infavor_position_num),3)*100
		against_percent = round(float(against_position_num) / float(against_position_num+infavor_position_num),3)*100

	total_positions = Postura.objects.all().order_by('-date_Postura')

	position_date = Postura.objects.filter(id_debate_id = id_debate).values("date_Postura")
	position_date_group = itertools.groupby(position_date, lambda record: record.get("date_Postura").strftime("%Y-%m-%d"))
	temp = 0
	positions_by_day = [[debate.date.strftime("%Y-%m-%d"),0]]
	for day,position in position_date_group:
		temp += len(list(position))
		positions_by_day.append([day, temp])
	# positions_by_day = json.dumps(positions_by_day)

	infavor_to_against = 0
	against_to_infavor = 0
	reason_infavor_to_against = []
	reason_against_to_infavor = []
	for i in range (1,4):
		num = Postura.objects.filter(id_debate_id=id_debate, postura=0, cambio_postura=i).count()
		reason_infavor_to_against.append(num)
		infavor_to_against += num
	for i in range (1,4):
		num = Postura.objects.filter(id_debate_id=id_debate, postura=1, cambio_postura=i).count()
		reason_against_to_infavor.append(num)
		against_to_infavor += num

	debate_members = "publico"
	participate = True
	members_list = []
	if debate.tipo_participacion == 1:
		debate_members = Participantes.objects.filter(id_debate_id=id_debate)
		for member in debate_members:
			user = User.objects.get(id=member.id_usuario_id)
			profile = Perfil.objects.get(user_id=user.id)
			members_list.append({'user':user, 'profile':profile})
		try:
			m = Participantes.objects.get(id_debate_id=id_debate,id_usuario_id=actual_user_id)
		except:
			participate = False

	data = {'debate': debate,
		'owner_user': owner_user,
		'usuario': actual_user_id,
		'owner_profile': owner_profile,
		'actual_user_position': actual_user_position,
		'infavor_args_list': infavor_args_list, 'against_args_list': against_args_list,
		'can_argue': can_argue, 'p_post': can_change_position,
		'infavor_position_num': infavor_position_num, 'against_position_num': against_position_num,
		'infavor_percent': infavor_percent, 'against_percent': against_percent,
		'infavor_to_against':infavor_to_against, 'against_to_infavor':against_to_infavor,
		'reason_infavor_to_against':reason_infavor_to_against, 'reason_against_to_infavor':reason_against_to_infavor,
		'counterarg_num':counterarg_num, 'arg_form1':arg_form1,
		'arg_form0':arg_form0,'counterarg_form':counterarg_form,
		'participate': participate, 'debate_members': members_list, 'counterarg_type': counterarg_type,
		'counterarg_target': counterarg_target, 'visits': visits, 'positions_by_day':positions_by_day}
	return render(request, 'debate.html', data)

def argumentData(arguments, actual_user, counterarg_num, id_debate):
	args_list = []
	for arg in arguments:
		counterargs = Respuesta.objects.filter(id_argumento_id= arg.id_argumento)
		counterargs_actual_user_num = Respuesta.objects.filter(id_usuario_id=actual_user, id_argumento_id= arg.id_argumento).count()
		counterargs_list = []
		can_counterarg = True
		for counterarg in counterargs:
			id = counterarg.id_respuesta
			text = counterarg.descripcion
			owner = User.objects.get(id=counterarg.id_usuario_id)
			if counterarg.alias_c == "alias":
				alias = Perfil.objects.get(user= owner)
				owner = alias.alias
			else:
				owner = owner.username
			counterargs_list.append({'text': text, 'owner': owner,
									'id': id, 'id_owner': counterarg.id_usuario_id})
			if counterargs_actual_user_num < counterarg_num:
				can_counterarg = True
			else:
				can_counterarg = False
		owner_arg = User.objects.get(id= arg.id_usuario_id)
		if (arg.alias_c == "alias"):
			owner_profile = Perfil.objects.get(user=owner_arg)
			owner_arg = owner_profile.alias
		try:
			rate = Valoracion.objects.get(id_argumento_id= arg.id_argumento, id_usuario_id = actual_user, tipo_valoracion="sumar")
			positive_rate_exist = "si"
		except:
			positive_rate_exist = "no"
		try:
			rate = Valoracion.objects.get(id_argumento_id= arg.id_argumento, id_usuario_id = actual_user, tipo_valoracion="quitar")
			negative_rate_exist = "si"
		except:
			negative_rate_exist = "no"
		exist_rate=[positive_rate_exist,negative_rate_exist]
		positive_rate = Valoracion.objects.filter(id_argumento_id= arg.id_argumento, tipo_valoracion="sumar").count()
		negative_rate = Valoracion.objects.filter(id_argumento_id= arg.id_argumento, tipo_valoracion="quitar").count()
		total_rate = positive_rate - negative_rate
		arg.puntaje = total_rate
		arg.save()
		position_owner_arg = Postura.objects.get(id_usuario_id= arg.id_usuario_id, id_debate_id=id_debate).postura
		args_list.append({'text': arg.descripcion, 'owner_arg': owner_arg, 'rate': total_rate,
							'id_arg': arg.id_argumento, 'exist_rate': exist_rate, 'owner_arg_id': owner_arg.id, 'counterargs': counterargs_list,
							'can_counterarg': can_counterarg})
	return args_list

##@brief Funcion que guarda el comentario del usuario de un argumento.
##@param request solicitud web, entrega los datos del usuario actual
##@return id_debat para redireccional a la vista "showDebate" con este id de debate
##@warning Login is required
@login_required
def newCounterargument(request,id_debate, id_argumento):
	if request.method == "POST":
		id_arg = request.POST[id_argumento]
		counterarg_form = newCounterargForm(request.POST, creador=0, max_length=0)
		if counterarg_form.is_valid():
			post = counterarg_form.save(commit=False)
			post.id_usuario_id = request.user.id
			post.id_argumento_id = id_arg
			post.save()
		updateReputation(request.user.id, 3)
	return counterarg_form

def updateReputation(id_usr, score):
    profile = Perfil.objects.get(user_id=id_usr)
    reputation = profile.reputacion + score
    profile.reputacion = reputation
    profile.save()

##@brief Funcion que guarda la valoracion del usuario al argumento
##@param request solicitud web, entrega los datos del usuario actual
##@return respuesta se ingresa en el HttpResponse para indicar la valoracion actualizada del argumento
##@warning Login is required
@login_required
def rateArgument(request):
	rate_argument= request.POST['id_arg']
	rate=request.POST['opcion']
	if rate == "sumar":
		score = 4
	elif rate =="quitar":
		score = -2
	elif rate =="nulo-sumar":
		score = -4
	elif rate =="nulo-quitar":
		score = 2
	try:
		rate_post = Valoracion.objects.get(id_argumento_id=rate_argument, id_usuario_id=request.user.id);
		actual_rate = rate_post.tipo_valoracion
		if rate == "sumar" or rate == "quitar":
			if actual_rate == "sumar":
				score -= 4
			elif actual_rate == "quitar":
				score += 2
		rate_post.tipo_valoracion = rate
	except:
		rate_post = Valoracion(id_argumento_id=rate_argument, id_usuario_id=request.user.id, tipo_valoracion=rate)
	rate_post.save()
	id_owner_arg = Argumento.objects.get(id_argumento=rate_argument).id_usuario_id
	updateReputation(id_owner_arg, score)
	positive_rate = Valoracion.objects.filter(id_argumento_id= rate_argument, tipo_valoracion="sumar").count()
	negative_rate = Valoracion.objects.filter(id_argumento_id= rate_argument, tipo_valoracion="quitar").count()
	total_rate = positive_rate - negative_rate
	return(total_rate)

def elimina_argumento(request):
	id_arg = request.POST['id_arg_delete']
	id_deb=request.POST['id_deb_arg_eliminar']
	arg = Argumento.objects.get(pk=id_arg)
	arg.delete()
	updateReputation(request.user.id, -3)
	return (id_deb)

def ver_notificacion(request, id_debate, id_notificacion):
	notification = Notificacion.objects.get(id=id_notificacion)
	notification.estado = 1
	notification.save()
	return redirect(showDebate,id_debate)

def visitCount(debate, usuario):
	utc=pytz.UTC
	try:
		visit = Visita.objects.get(id_debate=debate, id_usuario_id=usuario.id)
		delta = visit.date + timedelta(minutes=30)
	except:
		visit = Visita.objects.create(id_debate=debate, id_usuario_id=usuario.id)
		delta = utc.localize(visit.date) + timedelta(minutes=30)
	ahora = utc.localize(datetime.datetime.today())
	if delta <= ahora:
		visit.num = visit.num + 1
		visit.date = ahora
		visit.save()
	total = Visita.objects.filter(id_debate=debate).aggregate(Sum('num'))
	return total.values()[0]
