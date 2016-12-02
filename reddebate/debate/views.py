from django.shortcuts import render, redirect

from resumen.models import Usuario, Debate, Postura, Argumento

from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def despliega(request, id_debate): #debate_id
	if request.method == 'POST':
		if 'postu' in request.POST:
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
			return HttpResponse(resp)

		if 'descripcion' in request.POST:
			print("post_arg de despliega")
			descrip = request.POST['descripcion']
			postura_deb_usr = request.POST['postura']
			print(postura_deb_usr)
			usuario = request.user
			print(request.user)
			id_debat = request.POST['id_deb']
			publicar= Argumento(descripcion=descrip, id_usuario_id=usuario.id, id_debate_id=id_debat, postura= postura_deb_usr)
			publicar.save()
			print (Argumento.objects.filter(id_debate_id= id_debat))
			return redirect(despliega,id_debat)

	debate = Debate.objects.get(id_debate= id_debate)
	usuario_id = debate.id_usuario_id #usuario creador 
	usuario_debate = User.objects.get(id= usuario_id) 
	usuario_actual = request.user.id
	#que es mejor, tener la llave foranea a postura, y luego buscar en varias tablas, para armar el arreglo voy a 
	# usar varias decisiones. 

	argumentos_aFavor = Argumento.objects.filter(id_debate_id= id_debate, postura= 1) 
	argumentos_enContra = Argumento.objects.filter(id_debate_id= id_debate, postura= 0) 
	argumentos_F = []
	argumentos_C = []
	tiene_argumento ='no'
	for argumento in argumentos_aFavor:
		usuario_debate = User.objects.get(id= argumento.id_usuario_id) 
		argumentos_F.append([argumento.descripcion, usuario_debate] ) 

		if (request.user.id == argumento.id_usuario_id):
			tiene_argumento ='si'

	for argumento in argumentos_enContra:
		usuario_debate = User.objects.get(id= argumento.id_usuario_id) 
		argumentos_C.append([argumento.descripcion, usuario_debate] ) 
		if (request.user.id == argumento.id_usuario_id):
			tiene_argumento = 'si'
	print("argumentos: ", argumentos_C)
	try:
		postura_debate_usuario = Postura.objects.get(id_usuario_id= usuario_actual, id_debate_id=id_debate)
		tiene_postura = True
	except: 
		postura_debate_usuario = "No definido"
		tiene_postura = False

	print (debate)
	print (usuario_debate)
	print (tiene_argumento)
	#print (postura_debate_usuario)
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

	return render(request, 'debate.html', {'debate': debate, 'usuario': usuario_debate,
		'postura_usr_deb': postura_debate_usuario,
		'argF': argumentos_F, 'argC': argumentos_C, 't_arg': tiene_argumento,
		'num_post_f': numpost_f, 'num_post_c': numpost_c })
	#return render_to_response('debate.html', context)

