from django.shortcuts import render, render_to_response
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User

#from .forms import PostForm
from django.http import HttpResponse
#

#from .forms import PostForm
from django.shortcuts import redirect
import requests

# Create your views here.
from django.http import HttpResponse
from resumen.models import Perfil, Debate


def index(request):
    if request.method == 'POST':
        print("cerrado el debate", request.POST['id_deb'])
        id_deb = request.POST['id_deb']
        deb = Debate.objects.get(pk=id_deb)
        deb.estado = 'cerrado'
        deb.save()
    usuario = request.user
    u = User.objects.get(username= usuario.username)
    iniciando_alias(request, u)
    
    category_list = Debate.objects.all()
    usuario = request.user.id
    print("el usuario activo es_: ", usuario)
    context = {'object_list': category_list, 'usuario': usuario}
    return render(request, 'index.html', context)

def iniciando_alias(request, u):
    try:
        usuario_2 = Perfil.objects.get(user= u)
        print("en el try: alias_usuario")
        alias_usuario = usuario_2.alias
        print(alias_usuario)
    except:
        perfil_usuario= Perfil(user=u)
        perfil_usuario.save()
        usuario_2 = Perfil.objects.get(user= u)
        alias_usuario = usuario_2.alias

        print("en el except: alias_usuario")
        print(alias_usuario)



#Formulario
# def post_new(request):
#         form = PostForm()
#         return render(request, 'post_edit.html', {'form': form})

def post_new(request):

    if request.method == 'POST':
        ti = request.POST['titulo']
        des = request.POST['descripcion']
        largo_max = request.POST['largo_m']
        alias = request.POST['alias'] #check on, 
        print("valor checkbox 'alias':")
        
        print(alias)

        usuario = request.user
        print (usuario.id)
        publicar= Debate(titulo=ti, descripcion=des, id_usuario_id=usuario.id, largo=largo_max, alias_c=alias)
        publicar.save()
        return redirect('index')
    usuario = request.user
    u = User.objects.get(username= usuario.username)
    usuario_2 = Perfil.objects.get(user= u)
    alias_usuario = usuario_2.alias
#alias_usuario = u.Usuario.alias
    context = {'nombre':usuario.username,'alias': alias_usuario }
    return render(request, 'post_edit.html', context)
