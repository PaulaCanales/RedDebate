from django.shortcuts import render, render_to_response
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
import datetime

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
    for debate in category_list:
        ahora = datetime.date.today()
        print("ahora: ")
        print(ahora)
        print (debate.date_fin)
        if debate.date_fin!= None and debate.date_fin <= ahora :
           
            debate.estado = 'cerrado'
            debate.save()
            print(debate)
    usuario = request.user #usuario actual id
    print("el usuario activo es_: ", usuario.id)
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
        alias = request.POST['alias']
        fecha_fin = request.POST['date']
        print(fecha_fin)
        print("valor checkbox 'alias':")
        
        print(alias)

        usuario = request.user
        print (usuario.id)
        publicar= Debate(titulo=ti, descripcion=des, id_usuario_id=usuario.id,
            largo=largo_max, alias_c=alias, date_fin= fecha_fin)
        publicar.save()
        return redirect('index')

    usuario = request.user
    u = User.objects.get(username= usuario.username)
    usuario_2 = Perfil.objects.get(user= u)
    alias_usuario = usuario_2.alias
#alias_usuario = u.Usuario.alias
    context = {'nombre':usuario.username,'alias': alias_usuario, 'usuario': usuario }
    return render(request, 'post_edit.html', context)

def perfil(request, id_usuario):
    if request.method == 'POST':
        nuevo_alias = request.POST['nuevo_alias']
        usuario = request.user
        print (usuario.id)
        publicar= Perfil.objects.get(user=usuario)
        publicar.alias = nuevo_alias
        publicar.save()
        return redirect('perfil', 2)

    print(id_usuario)
    usuario = User.objects.get(id= id_usuario)
    alias_usuario = Perfil.objects.get(user=usuario)
    debates_abiertos = Debate.objects.filter(id_usuario_id= id_usuario, estado= 'abierto')
    debates_cerrados = Debate.objects.filter(id_usuario_id= id_usuario, estado= 'cerrado')
    
    print("llega al perfil")
    
    return render(request, 'perfil_usuario.html', {'usuario': usuario,
        'alias': alias_usuario,
        'debates_abiertos': debates_abiertos,
        'debates_cerrados': debates_cerrados,
        })

