from django.shortcuts import render

from resumen.models import Usuario, Debate, Postura

from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def despliega(request, id_debate): #debate_id
	if request.method == 'POST' and ('postu' in request.POST):
		
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
			resp="a favor!"
		else:
			resp="en contra!"
		return HttpResponse(resp)

	debate = Debate.objects.get(id_debate= id_debate)
	usuario_id = debate.id_usuario_id #usuario creador 
	usuario_debate = User.objects.get(id= usuario_id)
	try:
		postura_debate_usuario = Postura.objects.get(id_usuario_id= request.user.id, id_debate_id=id_debate)
		tiene_postura = True
	except: 
		postura_debate_usuario = "No definido"
		tiene_postura = False
	print (debate)
	print (usuario_debate)
	#print (postura_debate_usuario)
	if tiene_postura:
		if postura_debate_usuario.postura == 1:
			postura_debate_usuario = "A favor"
		else:
			postura_debate_usuario = "En contra"
	return render(request, 'debate.html', {'debate': debate, 'usuario': usuario_debate, 'postura_usr_deb': postura_debate_usuario })
	#return render_to_response('debate.html', context)
	
	

def post_arg(request):
	print("post_arg")
	if request.method == 'POST':
		des = request.POST['descripcion']
		usuario = request.user
		debate = id_deb
		publicar= Argumento(descripcion=des, id_usuario_id=usuario, id_debate_id=debate)
		publicar.save()
		return redirect(debate)
	return render(request, 'post_edit.html')

