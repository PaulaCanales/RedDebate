from django.shortcuts import render, redirect

from resumen.models import Debate
from debate.models import Postura, Argumento, Valoracion, Respuesta, Edicion, Participantes, Visita
from perfil.models import Perfil, Notificacion
from debate.forms import publicaArgumentoForm1,publicaArgumentoForm0, publicaRespuestaForm
from resumen.views import verificaNotificacion

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import *
import itertools
import json
import datetime
import pytz

##@brief Funcion que despliega el debate
##@param request solicitud web
##@param id_debate id del debate solicitado por la url dinamica
##@return render redirecciona a "Debate" si el debate esta abierto y "debate_cerrado" si no
##@warning Login is required
@login_required
def despliega(request, id_debate): #debate_id
	max_length = Debate.objects.get(id_debate=id_debate).largo
	creador=[('username', User.objects.get(id=request.user.id).username),
	         ('alias',Perfil.objects.get(user= request.user).alias)]
	arg_form0 = publicaArgumentoForm0(creador=creador,max_length=max_length)
	arg_form1 = publicaArgumentoForm1(creador=creador,max_length=max_length)
	resp_form = publicaRespuestaForm(creador=creador,max_length=max_length)
	debate = Debate.objects.get(id_debate= id_debate)
	vistas = cuenta_visitas(debate, request.user)
	if request.method == 'POST':
		# visita = Visita.objects.filter(id_debate=debate)
		# visita.update(num=visita.num-1)
		if 'id_arg' in request.POST:
			respuesta = valorar_argumento(request)
			return HttpResponse(respuesta)

		if 'responder0' in request.POST:
			resp_form = publica_redate(request, id_debate, "id_argumento0")
			return redirect(despliega,id_debate)

		if 'responder1' in request.POST:
			resp_form = publica_redate(request, id_debate, "id_argumento1")
			return redirect(despliega,id_debate)

		if 'id_arg_eliminar' in request.POST:
			id_debate = elimina_argumento(request)
			return redirect(despliega,id_debate)

	usuario_id = debate.id_usuario_id #usuario creador
	usuario_creador = User.objects.get(id= usuario_id)
	cant_rebates = debate.num_rebate
	cant_argumentos = debate.num_argumento
	cant_cambio_postura = debate.num_cambio_postura
	tipo_rebate = debate.tipo_rebate
	try:
		perfil_creador = Perfil.objects.get(user= usuario_creador)
		perfil_creador = perfil_creador.alias
	except:
		perfil_creador = 'username'

	usuario_actual = request.user
	usuario_actual_alias = Perfil.objects.get(user= usuario_actual)
	usuario_actual = usuario_actual.id

	argumentos_aFavor = Argumento.objects.filter(id_debate_id= id_debate, postura= 1)
	argumentos_enContra = Argumento.objects.filter(id_debate_id= id_debate, postura= 0)
	argumentos_F = []
	argumentos_C = []

	# tiene_argumento ='no'
	for argumento in argumentos_aFavor:
		ediciones = Edicion.objects.filter(id_argumento_id= argumento.id_argumento)
		redebates = Respuesta.objects.filter(id_argumento_id= argumento.id_argumento)
		rebates_usr = Respuesta.objects.filter(id_usuario_id=request.user, id_argumento_id= argumento.id_argumento).count()
		redebates_lista = []
		puede_rebatir1 = True
		for redebate in redebates:
			id_respuesta = redebate.id_respuesta
			descripcion_redebate = redebate.descripcion
			usuario_redebate = User.objects.get(id=redebate.id_usuario_id)
			if redebate.alias_c == "alias":
				usuario_alias = Perfil.objects.get(user= usuario_redebate)
				usuario_redebate = usuario_alias.alias
			else:
				usuario_redebate = usuario_redebate.username

			redebates_lista.append({'descripcion': descripcion_redebate, 'usr_creador': usuario_redebate,
									'id_rebate': id_respuesta, 'id_creador': redebate.id_usuario_id})
			if rebates_usr < cant_rebates:
				puede_rebatir1 = True
			else:
				puede_rebatir1 = False
		usuario_debate = User.objects.get(id= argumento.id_usuario_id)
		usuario_id = usuario_debate.id
		if (argumento.alias_c == "alias"):
			usuario_alias = Perfil.objects.get(user=usuario_debate)
			usuario_debate = usuario_alias.alias
		try:
			valoracion = Valoracion.objects.get(id_argumento_id= argumento.id_argumento, id_usuario_id = usuario_actual, tipo_valoracion="sumar")
			t_valoracion_suma = "si"
		except:
			t_valoracion_suma = "no"
		try:
			valoracion = Valoracion.objects.get(id_argumento_id= argumento.id_argumento, id_usuario_id = usuario_actual, tipo_valoracion="quitar")
			t_valoracion_quita = "si"
		except:
			t_valoracion_quita = "no"
		t_valoracion=[t_valoracion_suma,t_valoracion_quita]
		val_sumar = Valoracion.objects.filter(id_argumento_id= argumento.id_argumento, tipo_valoracion="sumar").count()
		val_quitar = Valoracion.objects.filter(id_argumento_id= argumento.id_argumento, tipo_valoracion="quitar").count()
		valoracion_argF = val_sumar - val_quitar
		argumento.puntaje = valoracion_argF
		argumento.save()
		post_usr_arg = Postura.objects.get(id_usuario_id= argumento.id_usuario_id, id_debate_id=id_debate).postura
		argumentos_F.append({'descripcion': argumento.descripcion, 'usr_creador': usuario_debate, 'valoracion': valoracion_argF,
							'id_arg': argumento.id_argumento, 't_val': t_valoracion, 'id_creador': usuario_id, 'redebates': redebates_lista ,
							'rebatir': puede_rebatir1, 'alias': argumento.alias_c, 'postura':argumento.postura, 'postura_arg': post_usr_arg})

		# if (request.user.id == argumento.id_usuario_id):
		# 	tiene_argumento ='si'

	for argumento in argumentos_enContra:

		ediciones = Edicion.objects.filter(id_argumento_id= argumento.id_argumento)
		redebates = Respuesta.objects.filter(id_argumento_id= argumento.id_argumento)
		rebates_usr = Respuesta.objects.filter(id_usuario_id=request.user, id_argumento_id= argumento.id_argumento).count()
		redebates_lista = []
		puede_rebatir0 = True
		for redebate in redebates:
			id_respuesta = redebate.id_respuesta
			descripcion_redebate = redebate.descripcion
			usuario_redebate = User.objects.get(id=redebate.id_usuario_id)
			if redebate.alias_c == "alias":
				usuario_alias = Perfil.objects.get(user= usuario_redebate)
				usuario_redebate = usuario_alias.alias
			else:
				usuario_redebate = usuario_redebate.username

			redebates_lista.append({'descripcion': descripcion_redebate, 'usr_creador': usuario_redebate,
									'id_rebate': id_respuesta, 'id_creador': redebate.id_usuario_id})
			if rebates_usr < cant_rebates:
				puede_rebatir0 = True
			else:
				puede_rebatir0 = False
		usuario_debate = User.objects.get(id= argumento.id_usuario_id)
		usuario_id = usuario_debate.id

		if (argumento.alias_c == "alias"):
			usuario_alias = Perfil.objects.get(user=usuario_debate)
			usuario_debate = usuario_alias.alias
		try:
			valoracion = Valoracion.objects.get(id_argumento_id= argumento.id_argumento, id_usuario_id = request.user.id, tipo_valoracion="sumar")
			t_valoracion_suma = "si"
		except:
			t_valoracion_suma = "no"
		try:
			valoracion = Valoracion.objects.get(id_argumento_id= argumento.id_argumento, id_usuario_id = request.user.id, tipo_valoracion="quitar")
			t_valoracion_quita = "si"
		except:
			t_valoracion_quita = "no"
		val_sumar = Valoracion.objects.filter(id_argumento_id= argumento.id_argumento, tipo_valoracion="sumar").count()
		val_quitar = Valoracion.objects.filter(id_argumento_id= argumento.id_argumento, tipo_valoracion="quitar").count()
		valoracion_argC = val_sumar - val_quitar
		t_valoracion=[t_valoracion_suma,t_valoracion_quita]
		argumento.puntaje = valoracion_argC
		argumento.save()
		post_usr_arg = Postura.objects.get(id_usuario_id= argumento.id_usuario_id, id_debate_id=id_debate).postura
		argumentos_C.append({'descripcion': argumento.descripcion, 'usr_creador': usuario_debate,'valoracion': valoracion_argC,
							'id_arg':argumento.id_argumento,'t_val':t_valoracion,'id_creador':usuario_id,'redebates':redebates_lista,
							'rebatir': puede_rebatir0,'alias': argumento.alias_c, 'postura': argumento.postura, 'postura_arg': post_usr_arg })
		# if (request.user.id == argumento.id_usuario_id):
		# 	tiene_argumento = 'si'
	argumentos_C = sorted(argumentos_C, key=lambda valoracion: valoracion['valoracion'], reverse=True)
	argumentos_F = sorted(argumentos_F, key=lambda valoracion: valoracion['valoracion'], reverse=True)

	argumentos_usr = Argumento.objects.filter(id_debate_id= id_debate, id_usuario_id=request.user ).count()
	if argumentos_usr < cant_argumentos:
		puede_argumentar = True
	else:
		puede_argumentar = False

	try:
		postura_debate_usuario = Postura.objects.get(id_usuario_id= usuario_actual, id_debate_id=id_debate)
		tiene_postura = True
		cambios_usr = postura_debate_usuario.cuenta_cambios
	except:
		postura_debate_usuario = "No definido"
		tiene_postura = False
		cambios_usr = 0

	if cambios_usr < cant_cambio_postura:
		puede_cambiar_postura = True
	else:
		puede_cambiar_postura = False
	rebate = "Ambos"
	if tiene_postura:
		if postura_debate_usuario.postura == 1:
			postura_debate_usuario = "A Favor"
			if tipo_rebate == 1:
				rebate = "En Contra"
		else:
			postura_debate_usuario = "En Contra"
			if tipo_rebate == 1:
				rebate = "A Favor"
	posturas_f=Postura.objects.filter(id_debate_id=id_debate, postura=1)
	posturas_c=Postura.objects.filter(id_debate_id=id_debate, postura=0)
	numpost_f=posturas_f.count()
	numpost_c=posturas_c.count()
	if (int(numpost_c+numpost_f)==0):
		porcentaje_c=0
		porcentaje_f=0
	else:
		porcentaje_f = round(float(numpost_f) / float(numpost_c+numpost_f),3)*100
		porcentaje_c = round(float(numpost_c) / float(numpost_c+numpost_f),3)*100

	posturas_total = Postura.objects.all().order_by('-date_Postura')

	fecha = Postura.objects.filter(id_debate_id = id_debate).values("date_Postura")
	grupo = itertools.groupby(fecha, lambda record: record.get("date_Postura").strftime("%Y-%m-%d"))
	suma = 0
	posturas_por_dia = [[debate.date.strftime("%Y-%m-%d"),0]]
	for dia,postura_dia in grupo:
		suma += len(list(postura_dia))
		posturas_por_dia.append([dia, suma])
	# posturas_por_dia = [[dia, len(list(postura_dia)), suma+len(list(postura_dia))] for dia, postura_dia in grupo]
	# posturas_por_dia.insert(0,[debate.date.strftime("%Y-%m-%d"),0])
	print(posturas_por_dia)
	fecha_posturas = json.dumps(posturas_por_dia)
	cambio_favor_contra = 0
	cambio_contra_favor = 0
	razon_favor_contra = []
	razon_contra_favor = []
	for i in range (1,4):
		num = Postura.objects.filter(id_debate_id=id_debate, postura=0, cambio_postura=i).count()
		razon_favor_contra.append(num)
		cambio_favor_contra += num
	for i in range (1,4):
		num = Postura.objects.filter(id_debate_id=id_debate, postura=1, cambio_postura=i).count()
		razon_contra_favor.append(num)
		cambio_contra_favor += num
	notificacion_usr = verificaNotificacion(request)
	participantes = "publico"
	participa = True
	lista_participantes = []
	if debate.tipo_participacion == 1:
		participantes = Participantes.objects.filter(id_debate_id=id_debate)
		for participante in participantes:
			lista_participantes.append(User.objects.get(id=participante.id_usuario_id))
		try:
			p = Participantes.objects.get(id_debate_id=id_debate,id_usuario_id=usuario_actual)
		except:
			participa = False

	datos = {'debate': debate,
		'usuario_creador': usuario_creador,
		'usuario': usuario_actual,
		'alias': perfil_creador,
		'alias_actual': usuario_actual_alias.alias,
		'postura_usr_deb': postura_debate_usuario,
		'argF': argumentos_F, 'argC': argumentos_C, 't_arg': puede_argumentar, 'p_post': puede_cambiar_postura,
		'num_post_f': numpost_f, 'num_post_c': numpost_c,
		'porc_f': porcentaje_f, 'porc_c': porcentaje_c,
		'cambio_f_c':cambio_favor_contra, 'cambio_c_f':cambio_contra_favor,
		'razon_f_c':razon_favor_contra, 'razon_c_f':razon_contra_favor,
		'img': debate.img, 'cant_rebates':cant_rebates, 'arg_form1':arg_form1,
		'arg_form0':arg_form0,'resp_form':resp_form, 'notificaciones': notificacion_usr,
		'participa': participa, 'participantes': lista_participantes, 'tipo_rebate': tipo_rebate,
		'rebate': rebate, 'visitas': vistas, 'fecha_posturas':posturas_por_dia}
	return render(request, 'debate.html', datos)

##@brief Funcion que guarda el comentario del usuario de un argumento.
##@param request solicitud web, entrega los datos del usuario actual
##@return id_debat para redireccional a la vista "despliega" con este id de debate
##@warning Login is required
@login_required
def publica_redate(request,id_debate, id_argumento):
	if request.method == "POST":
		id_arg = request.POST[id_argumento]
		print(id_arg)
		resp_form = publicaRespuestaForm(request.POST, creador=0, max_length=0)
		if resp_form.is_valid():
			post = resp_form.save(commit=False)
			post.id_usuario_id = request.user.id
			post.id_argumento_id = id_arg
			post.save()
		actualiza_reputacion(request.user.id, 3)
	return resp_form

def actualiza_reputacion(id_usr, puntaje):
    perfil = Perfil.objects.get(user_id=id_usr)
    reputacion = perfil.reputacion + puntaje
    perfil.reputacion = reputacion
    perfil.save()

##@brief Funcion que guarda la valoracion del usuario al argumento
##@param request solicitud web, entrega los datos del usuario actual
##@return respuesta se ingresa en el HttpResponse para indicar la valoracion actualizada del argumento
##@warning Login is required
@login_required
def valorar_argumento(request):
	print("valorar argumento")
	val_argumento= request.POST['id_arg']
	usuario = request.user
	val=request.POST['opcion']
	if val == "sumar":
		puntaje = 4
	elif val =="quitar":
		puntaje = -2
	elif val =="nulo-sumar":
		puntaje = -4
	elif val =="nulo-quitar":
		puntaje = 2
	try:
		publicar = Valoracion.objects.get(id_argumento_id=val_argumento, id_usuario_id=usuario.id);
		val_actual = publicar.tipo_valoracion
		if val == "sumar" or val == "quitar":
			if val_actual == "sumar":
				puntaje -= 4
			elif val_actual == "quitar":
				puntaje += 2
		publicar.tipo_valoracion = val
	except:
		publicar = Valoracion(id_argumento_id=val_argumento, id_usuario_id=usuario.id, tipo_valoracion=val)
	publicar.save()
	id_usr_arg = Argumento.objects.get(id_argumento=val_argumento).id_usuario_id
	actualiza_reputacion(id_usr_arg, puntaje)
	val_sumar = Valoracion.objects.filter(id_argumento_id= val_argumento, tipo_valoracion="sumar").count()
	val_quitar = Valoracion.objects.filter(id_argumento_id= val_argumento, tipo_valoracion="quitar").count()
	respuesta = val_sumar - val_quitar
	return(respuesta)

def elimina_argumento(request):
	id_argumento = request.POST['id_arg_eliminar']
	id_deb=request.POST['id_deb_arg_eliminar']
	arg = Argumento.objects.get(pk=id_argumento)
	arg.delete()
	actualiza_reputacion(request.user.id, -3)
	return (id_deb)

def ver_notificacion(request, id_debate, id_notificacion):
	print("ver notificacion")
	notificacion = Notificacion.objects.get(id=id_notificacion)
	notificacion.estado = 1
	notificacion.save()
	return redirect(despliega,id_debate)

def cuenta_visitas(debate, usuario):
	utc=pytz.UTC
	try:
		vista = Visita.objects.get(id_debate=debate, id_usuario_id=usuario.id)
		delta = vista.date + timedelta(minutes=30)

	except:
		vista = Visita.objects.create(id_debate=debate, id_usuario_id=usuario.id)
		delta = utc.localize(vista.date) + timedelta(minutes=30)
	ahora = utc.localize(datetime.datetime.today())

	if delta <= ahora:
		vista.num = vista.num + 1
		vista.date = ahora
		vista.save()
	total = Visita.objects.filter(id_debate=debate).aggregate(Sum('num'))
	print(total)
	return total.values()[0]
