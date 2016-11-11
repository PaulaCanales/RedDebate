from django.shortcuts import render

from resumen.models import Usuario, Debate

from django.http import HttpResponse


# Create your views here.
def despliega(request, id_debate): #debate_id
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
	