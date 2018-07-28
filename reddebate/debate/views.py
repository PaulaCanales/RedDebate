from django.shortcuts import render, redirect

from resumen.models import Debate
from debate.models import Postura, Argumento, Valoracion, Respuesta, Edicion
from perfil.models import Perfil
from debate.forms import publicaArgumentoForm

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
	arg_form = publicaArgumentoForm(creador=creador,max_length=max_length)
	if request.method == 'POST':
		if 'postura_debate_ajax' in request.POST:
			resp = define_postura(request)
			return HttpResponse(resp)
		if 'postura_debate' in request.POST:
			id_debate = define_postura(request)
			return redirect(despliega,id_debate)

		if 'descripcion' in request.POST:
			arg_form = publica_argumento(request, id_debate)
			return redirect(despliega,id_debate)

		if 'id_arg' in request.POST:
			respuesta = valorar_argumento(request)
			return HttpResponse(respuesta)

		if 'id_arg_rebate0' in request.POST:
			id_debat = publica_redate(request)
			return redirect(despliega,id_debat)

		if 'id_arg_rebate1' in request.POST:
			id_debat = publica_redate(request)
			return redirect(despliega,id_debat)

		if 'id_arg_eliminar' in request.POST:
			id_debate = elimina_argumento(request)
			return redirect(despliega,id_debate)

	debate = Debate.objects.get(id_debate= id_debate)
	usuario_id = debate.id_usuario_id #usuario creador
	usuario_creador = User.objects.get(id= usuario_id)
	cant_rebates = debate.num_rebate
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

	tiene_argumento ='no'
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

			redebates_lista.append([descripcion_redebate, usuario_redebate, id_respuesta])
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
		post_usr_arg = Postura.objects.get(id_usuario_id= argumento.id_usuario_id, id_debate_id=id_debate).postura
		argumentos_F.append([argumento.descripcion,
							usuario_debate,
							valoracion_argF,
							argumento.id_argumento,
							t_valoracion,
							usuario_id,
							redebates_lista ,
							puede_rebatir1,
							ediciones,
							argumento.alias_c,
							argumento.postura,
							post_usr_arg])

		if (request.user.id == argumento.id_usuario_id):
			tiene_argumento ='si'

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

			redebates_lista.append([descripcion_redebate, usuario_redebate, id_respuesta])
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
		post_usr_arg = Postura.objects.get(id_usuario_id= argumento.id_usuario_id, id_debate_id=id_debate).postura
		argumentos_C.append([argumento.descripcion,
							usuario_debate,
							valoracion_argC,
							argumento.id_argumento,
							t_valoracion,
							usuario_id,
							redebates_lista,
							puede_rebatir0,
							ediciones,
							argumento.alias_c,
							argumento.postura,
							post_usr_arg ])
		if (request.user.id == argumento.id_usuario_id):
			tiene_argumento = 'si'
	argumentos_C = sorted(argumentos_C, key=lambda valoracion: valoracion[2], reverse=True)
	argumentos_F = sorted(argumentos_F, key=lambda valoracion: valoracion[2], reverse=True)

	try:
		postura_debate_usuario = Postura.objects.get(id_usuario_id= usuario_actual, id_debate_id=id_debate)
		tiene_postura = True
	except:
		postura_debate_usuario = "No definido"
		tiene_postura = False
	if tiene_postura:
		if postura_debate_usuario.postura == 1:
			postura_debate_usuario = "A Favor"
		else:
			postura_debate_usuario = "En Contra"
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

	posturas_total = Postura.objects.filter(id_debate_id= id_debate)
	cambio_favor_contra = Postura.objects.filter(id_debate_id=id_debate, postura_inicial=0, postura=1).count()
	cambio_contra_favor = Postura.objects.filter(id_debate_id=id_debate, postura_inicial=1, postura=0).count()

	razon_favor_contra = []
	razon_contra_favor = []
	for i in range (1,4):
		razon_favor_contra.append(Postura.objects.filter(id_debate_id=id_debate, postura_inicial=0, postura=1, cambio_postura=i).count())
	for i in range (1,4):
		razon_contra_favor.append(Postura.objects.filter(id_debate_id=id_debate, postura_inicial=1, postura=0, cambio_postura=i).count())
	datos = {'debate': debate,
		'usuario_creador': usuario_creador,
		'usuario': usuario_actual,
		'alias': perfil_creador,
		'alias_actual': usuario_actual_alias.alias,
		'postura_usr_deb': postura_debate_usuario,
		'argF': argumentos_F, 'argC': argumentos_C, 't_arg': tiene_argumento,
		'num_post_f': numpost_f, 'num_post_c': numpost_c,
		'porc_f': porcentaje_f, 'porc_c': porcentaje_c,
		'cambio_f_c':cambio_favor_contra, 'cambio_c_f':cambio_contra_favor,
		'razon_f_c':razon_favor_contra, 'razon_c_f':razon_contra_favor,
		'img': debate.img, 'cant_rebates':cant_rebates, 'arg_form':arg_form}
	return render(request, 'debate.html', datos)


##@brief Funcion que guarda la postura del usuario en el debate, si esta ya existe la cambia, sino la crea.
##@param request solicitud web, entrega los datos del usuario actual
##@return resp que se ingresa en el HttpResponse para indicar la postura actualizada del usuario
##@warning Login is required
@login_required
def define_postura(request):
	id_debat= request.POST['id']
	usuario = request.user

	if 'postura_debate_ajax' in request.POST:
		post_usuario= request.POST['postura_debate_ajax']
		try:
			publicar_postura = Postura.objects.get(id_debate_id=id_debat, id_usuario_id=usuario.id)
			publicar_postura.postura=post_usuario
		except:
			publicar_postura = Postura(postura=post_usuario, postura_inicial=post_usuario, id_debate_id=id_debat, id_usuario_id=usuario.id)
		publicar_postura.save()
		if post_usuario=='1': resp= "A Favor"
		else: resp= "En Contra"

		return (resp)

	if 'postura_debate' in request.POST:
		post_usuario= request.POST['postura_debate']
		razon_cambio = request.POST['razon']
		try:
			publicar_postura = Postura.objects.get(id_debate_id=id_debat, id_usuario_id=usuario.id)
			publicar_postura.postura=post_usuario
			publicar_postura.cambio_postura=razon_cambio
		except:
			print("Error en publicar_postura")

		try:
			argumento = Argumento.objects.get(id_debate_id=id_debat, id_usuario_id =usuario.id)
			if(int(argumento.postura)!=int(publicar_postura.postura)):
				marcar_argumento=argumento.id_argumento
			else:
				marcar_argumento = "vacio"
		except:
			marcar_argumento = "vacio"


		publicar_postura.save()
		'''if (Argumento.objects.filter(id_debate_id=id_debat, id_usuario_id=usuario.id).count() >0):
			argumento_eliminar =Argumento.objects.get(id_debate_id=id_debat, id_usuario_id =usuario.id)
			argumento_eliminar.delete()'''

		return (id_debat)

##@brief Funcion que guarda el argumento del usuario en el debate, tambien edita el argumento.
##@param request solicitud web, entrega los datos del usuario actual
##@return id_debat para redireccionar a la vista "despliega" con este id de debate
##@warning Login is required
@login_required
def publica_argumento(request, id_debate):
	postura = Postura.objects.get(id_debate_id=id_debate, id_usuario_id = request.user)
	if request.method == "POST":
		arg_form = publicaArgumentoForm(request.POST, creador=0, max_length=0)
		if arg_form.is_valid():
			post = arg_form.save(commit=False)
			post.id_usuario_id = request.user.id
			post.id_debate_id = id_debate
			post.postura = postura.postura
			post.save()
	return arg_form

##@brief Funcion que guarda el comentario del usuario de un argumento.
##@param request solicitud web, entrega los datos del usuario actual
##@return id_debat para redireccional a la vista "despliega" con este id de debate
##@warning Login is required
@login_required
def publica_redate(request):
	descrip = request.POST['descripcion_rebate']
	try:
		argumento_debate = request.POST['id_arg_rebate0']
	except:
		argumento_debate = request.POST['id_arg_rebate1']
	id_debat = request.POST['id_deb']
	usuario = request.user
	if 'alias' in request.POST:
		alias_usuario = request.POST['alias']

		publicar= Respuesta(descripcion=descrip, id_usuario_id=usuario.id,
		 		id_argumento_id=argumento_debate, alias_c=alias_usuario)
	else :
		publicar= Respuesta(descripcion=descrip, id_usuario_id=usuario.id,
		 		id_argumento_id=argumento_debate)
	publicar.save()
	return(id_debat)

##@brief Funcion que guarda la valoracion del usuario al argumento
##@param request solicitud web, entrega los datos del usuario actual
##@return respuesta se ingresa en el HttpResponse para indicar la valoracion actualizada del argumento
##@warning Login is required
@login_required
def publica_valoracion(request):
	val_argumento= request.POST['id_arg']
	usuario = request.user
	val=request.POST['opcion']
	if val=="sumar":
		publicar_valoracion = Valoracion(id_argumento_id=val_argumento, id_usuario_id=usuario.id)
		publicar_valoracion.save()
		reputacion = 10
	elif val=="quitar":
		quitar_valoracion = Valoracion.objects.get(id_argumento_id=val_argumento, id_usuario_id=usuario.id);
		quitar_valoracion.delete()
		reputacion = -10
	respuesta = Valoracion.objects.filter(id_argumento_id = val_argumento).count()
	val_reputacion = request.POST['id_arg']
	usuario_argumento = Argumento.objects.get(id_argumento=val_reputacion).id_usuario_id
	usuario_reputacion = Perfil.objects.get(user_id=usuario_argumento).reputacion
	usuario_reputacion = usuario_reputacion + reputacion
	aumentar_reputacion = Perfil(user_id=usuario_argumento, reputacion=usuario_reputacion)
	aumentar_reputacion.save()
	return(respuesta)

def valorar_argumento(request):
	val_argumento= request.POST['id_arg']
	usuario = request.user
	val=request.POST['opcion']
	try:
		publicar = Valoracion.objects.get(id_argumento_id=val_argumento, id_usuario_id=usuario.id);
		publicar.tipo_valoracion = val
	except:
		publicar = Valoracion(id_argumento_id=val_argumento, id_usuario_id=usuario.id, tipo_valoracion=val)
	publicar.save()

	val_sumar = Valoracion.objects.filter(id_argumento_id= val_argumento, tipo_valoracion="sumar").count()
	val_quitar = Valoracion.objects.filter(id_argumento_id= val_argumento, tipo_valoracion="quitar").count()
	respuesta = val_sumar - val_quitar
	reputacion = val_sumar*5 - val_quitar*2
	usuario_argumento = Argumento.objects.get(id_argumento=val_argumento).id_usuario_id
	publicar_reputacion = Perfil.objects.get(user_id=usuario_argumento)
	publicar_reputacion.reputacion = reputacion
	publicar_reputacion.save()

	return(respuesta)

def elimina_argumento(request):
	id_argumento = request.POST['id_arg_eliminar']
	id_deb=request.POST['id_deb_arg_eliminar']
	arg = Argumento.objects.get(pk=id_argumento)
	arg.delete()
	return (id_deb)
