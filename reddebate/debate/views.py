from django.shortcuts import render

from resumen.models import Usuario, Debate, Postura

from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def despliega(request, id_debate): #debate_id
	if request.method == 'POST':
		
		post_usuario= request.POST['postu'] 
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

	debate = Debate.objects.filter(id_debate= id_debate)
	#usuario = User.objects.filter(id_usuario= debate.id_usuario_id)
	print (debate)
	return render(request, 'debate.html', {'debate': debate })
	#return render_to_response('debate.html', context)
	
	

	#def despliega_postura(request): 
	#	if request.method == 'POST': 
		#postura= request.POST['postu'] 
		#id_debate = request.POST['id'] 
		#postura = request.postu 
		#id_debate = request.id id_usuario = 1; 
		#if la postura ya existe, hay que sobreescribirla. 
		#publicar = Postura(postura=postura, id_debate_id=id_debate, id_usuario_id=id_usuario); 
		#publicar.save(); 
		#return ("hola")