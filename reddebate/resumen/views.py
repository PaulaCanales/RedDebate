from django.shortcuts import render, render_to_response
from django.views.generic import ListView, DetailView

#from .forms import PostForm
from django.http import HttpResponse
#

#from .forms import PostForm
from django.shortcuts import redirect
import requests

# Create your views here.
from django.http import HttpResponse
from resumen.models import Usuario, Debate


def index(request):
    if request.method == 'POST':
        print("cerrado el debate", request.POST['id_deb'])
        id_deb = request.POST['id_deb']
        deb = Debate.objects.get(pk=id_deb)
        deb.estado = 'cerrado'
        deb.save()
    category_list = Debate.objects.all()
    context = {'object_list': category_list}
    return render(request, 'index.html', context)



#Formulario
# def post_new(request):
#         form = PostForm()
#         return render(request, 'post_edit.html', {'form': form})

def post_new(request):

    if request.method == 'POST':
        ti = request.POST['titulo']
        des = request.POST['descripcion']
        publicar= Debate(titulo=ti, descripcion=des, id_usuario_id=1)
        publicar.save()
        return redirect('index')
    return render(request, 'post_edit.html')
