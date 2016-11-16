from django.shortcuts import render

from resumen.models import Usuario, Debate, Postura

from django.http import HttpResponse


# Create your views here.
def despliega(request, id_debate): #debate_id
	if request.method == 'POST':
		
		print("holaa")
		print(request.POST['postu'] )
		post= request.POST['postu'] 

		id_debat= request.POST['id'] 
		print(id_debat)
		print(post)
		id_usuario = 1
		try:
			publicar_postura = Postura.objects.get(id_debate_id=id_debat, id_usuario_id=id_usuario)
			publicar_postura.postura=post
		except:
			publicar_postura = Postura(postura=post, id_debate_id=id_debat, id_usuario_id=1)
			print(publicar_postura)
		publicar_postura.save() 
		if post=='1' :
			resp="a favor!"
		else:
			resp="en contra!"
		return HttpResponse(resp)

	print(id_debate)
	#if request.method == 'POST':
	#id_debate = request.POST
	print(id_debate)
	debate = Debate.objects.filter(id_debate= id_debate)
	#usuario = Usuario.objects.filter(id_usuario = .id_usuario)
	#print(usuario)
	
	#template = loader.get_template('debate.html')
	#return HttpResponse(template.render(context, request))
	
	#{'debate': <QuerySet [<Debate: Voto electronico>]>}
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