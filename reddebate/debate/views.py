from django.shortcuts import render, redirect

from resumen.models import Perfil, Debate, Postura, Argumento, Valoracion, Respuesta

from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def despliega(request, id_debate): #debate_id
	if request.method == 'POST':
		if 'postu' in request.POST:
			resp = define_postura(request)
			return HttpResponse(resp)

		if 'descripcion' in request.POST:
			id_debat = publica_argumento(request)
			return redirect(despliega,id_debat)

		if 'id_arg' in request.POST:
			respuesta = publica_valoracion(request)
			return HttpResponse(respuesta)

		if 'id_arg_rebate' in request.POST:
			id_debat = publica_redate(request)
			return redirect(despliega,id_debat)

	debate = Debate.objects.get(id_debate= id_debate)
	usuario_id = debate.id_usuario_id #usuario creador 
	usuario_creador = User.objects.get(id= usuario_id) 
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
		redebates = Respuesta.objects.filter(id_argumento_id= argumento.id_argumento)
		redebates_lista = []
		tiene_comentario = "no_comentario"
		for redebate in redebates:
			descripcion_redebate = redebate.descripcion
			usuario_redebate = User.objects.get(id=redebate.id_usuario_id)
			redebates_lista.append([descripcion_redebate, usuario_redebate])
			if tiene_comentario == "no_comentario" and usuario_redebate == request.user:
				tiene_comentario = "si_comentario"
		usuario_debate = User.objects.get(id= argumento.id_usuario_id)
		usuario_id = usuario_debate.id
		if (argumento.alias_c == "alias"): 
			usuario_alias = Perfil.objects.get(user=usuario_debate)
			usuario_debate = usuario_alias.alias
		try: 
			valoracion = Valoracion.objects.get(id_argumento_id= argumento.id_argumento, id_usuario_id = usuario_actual)
			t_valoracion = "si"
		except:
			t_valoracion = "no"
		print(usuario_debate)
		valoracion_argF = Valoracion.objects.filter(id_argumento_id= argumento.id_argumento).count()
		argumentos_F.append([argumento.descripcion, usuario_debate, 
			valoracion_argF, argumento.id_argumento, t_valoracion, usuario_id, redebates_lista , tiene_comentario]) 

		if (request.user.id == argumento.id_usuario_id):
			tiene_argumento ='si'

	for argumento in argumentos_enContra:

		redebates = Respuesta.objects.filter(id_argumento_id= argumento.id_argumento)
		redebates_lista = []
		tiene_comentario = "no_comentario"
		for redebate in redebates:
			descripcion_redebate = redebate.descripcion
			usuario_redebate = User.objects.get(id=redebate.id_usuario_id)
			redebates_lista.append([descripcion_redebate, usuario_redebate])
			if tiene_comentario == "no_comentario" and usuario_redebate == request.user:
				tiene_comentario = "si_comentario"
		usuario_debate = User.objects.get(id= argumento.id_usuario_id)
		usuario_id = usuario_debate.id

		if (argumento.alias_c == "alias"): 
			usuario_alias = Perfil.objects.get(user=usuario_debate)
			usuario_debate = usuario_alias.alias
		try: 
			valoracion = Valoracion.objects.get(id_argumento_id= argumento.id_argumento, id_usuario_id = request.user.id)
			t_valoracion = "si"
		except:
			t_valoracion = "no"
		valoracion_argC = Valoracion.objects.filter(id_argumento_id= argumento.id_argumento).count()

		argumentos_C.append([argumento.descripcion, usuario_debate,
		 valoracion_argC, argumento.id_argumento, t_valoracion, usuario_id, redebates_lista, tiene_comentario ]) 
		if (request.user.id == argumento.id_usuario_id):
			tiene_argumento = 'si'
	print("argumentos: ", argumentos_C)
	argumentos_C = sorted(argumentos_C, key=lambda valoracion: valoracion[2], reverse=True)
	print("argumentos: ", argumentos_C)
	argumentos_F = sorted(argumentos_F, key=lambda valoracion: valoracion[2], reverse=True)
	print("argumentos: ", argumentos_F)
	

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
	numpost_f=0
	numpost_c=0
	for postura in posturas_f:
		numpost_f+=1
	for postura in posturas_c:
		numpost_c+=1
	print(numpost_f)
	print(numpost_c)

	if debate.estado == 'abierto': 
		return render(request, 'debate.html', {'debate': debate,
			'usuario_creador': usuario_creador,
			'usuario': usuario_actual,
			'alias': perfil_creador,
			'alias_actual': usuario_actual_alias.alias,
			'postura_usr_deb': postura_debate_usuario,
			'argF': argumentos_F, 'argC': argumentos_C, 't_arg': tiene_argumento,
			'num_post_f': numpost_f, 'num_post_c': numpost_c })
	else:
		return render(request, 'debate_cerrado.html', {'debate': debate,
			'usuario_creador': usuario_creador,
			'usuario': usuario_actual,
			'alias': perfil_creador,
			'alias_actual': usuario_actual_alias.alias,
			'postura_usr_deb': postura_debate_usuario,
			'argF': argumentos_F, 'argC': argumentos_C, 't_arg': tiene_argumento,
			'num_post_f': numpost_f, 'num_post_c': numpost_c })
	#return render_to_response('debate.html', context)

def define_postura(request):
	post_usuario= request.POST['postu'] 
	print (post_usuario)
	id_debat= request.POST['id'] 
	usuario = request.user
	try:
		publicar_postura = Postura.objects.get(id_debate_id=id_debat, id_usuario_id=usuario.id)
		publicar_postura.postura=post_usuario
	except:
		publicar_postura = Postura(postura=post_usuario, id_debate_id=id_debat, id_usuario_id=usuario.id)
		print(publicar_postura)
	publicar_postura.save() 
	if post_usuario=='1' :
		resp= "A Favor"
	else:
		resp= "En Contra"
	return (resp)

def publica_argumento(request):
	print("post_arg de despliega")
	descrip = request.POST['descripcion']
	postura_deb_usr = request.POST['postura']
	usuario = request.user
	print(request.user)
	id_debat = request.POST['id_deb']
	try:
		publicar = Argumento.objects.get(id_usuario_id=usuario.id,id_debate_id=id_debat)
		publicar.descripcion = descrip
		if 'alias' in request.POST:
			alias_usuario = request.POST['alias']
			publicar.alias_c= alias_usuario
		else:
			publicar.alias_c= 'username'
	except: 
		if 'alias' in request.POST:
			alias_usuario = request.POST['alias']
			publicar= Argumento(descripcion=descrip, id_usuario_id=usuario.id,
		 		id_debate_id=id_debat, postura= postura_deb_usr, alias_c=alias_usuario)
		
		else :
			publicar= Argumento(descripcion=descrip, id_usuario_id=usuario.id,
		 		id_debate_id=id_debat, postura= postura_deb_usr)
	
	publicar.save()
	print (Argumento.objects.filter(id_debate_id= id_debat))
	return(id_debat)

def publica_redate(request):
	descrip = request.POST['descripcion_rebate']
	argumento_debate = request.POST['id_arg_rebate']
	print(argumento_debate)
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



def publica_valoracion(request):
	val_argumento= request.POST['id_arg'] 
	usuario = request.user
	publicar_valoracion = Valoracion(id_argumento_id=val_argumento, id_usuario_id=usuario.id)
	
	publicar_valoracion.save() 
	respuesta = Valoracion.objects.filter(id_argumento_id = val_argumento).count()
	return(respuesta)

