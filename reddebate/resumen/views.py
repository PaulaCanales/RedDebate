from django.shortcuts import render, render_to_response
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
from django.shortcuts import redirect
import requests

from django.http import HttpResponse
from resumen.models import Perfil, Debate, Postura

##@brief Funcion que despliega todos los debates
##@param request solicitud web
##@return render redirecciona a "index.html" con la lista de todos los debates
##@warning Login is required
@login_required
def index(request):
    if request.method == 'POST':
        if 'id_deb' in request.POST:
            cerrar_debate(request)
        if 'descripcion' in request.POST:
            resp = crear_debate(request)
            return redirect('index')

    usuario = request.user
    #u = User.objects.get(username= usuario.username)
    iniciando_alias(request, usuario)
    category_list = Debate.objects.all().order_by('-id_debate')
    for debate in category_list:
        ahora = datetime.date.today()
        if debate.estado != 'cerrado' and debate.date_fin!= None and debate.date_fin <= ahora :
            debate.estado = 'cerrado'
            debate.save()
            print(debate)
    print("el usuario activo es_: ", usuario.id)
    perfil_usuario = Perfil.objects.get(user_id= usuario.id)
    alias_usuario = perfil_usuario.alias
    context = {'object_list': category_list, 'usuario': usuario, 'alias': alias_usuario, }
    return render(request, 'index.html', context)

##@brief Funcion que inicializa el alias del usuario actual, en caso de no tener alias sera "anonimo".
##@param request solicitud web
##@param u usuario a crear alias. 
##@warning Login is required
@login_required
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

##@brief Funcion que cierra el debate
##@param request solicitud web
##@return redirect redirecciona a la vista "index"
##@warning Login is required
@login_required
def cerrar_debate(request):
    print("cerrado el debate", request.POST['id_deb'])
    id_deb = request.POST['id_deb']
    deb = Debate.objects.get(pk=id_deb)
    deb.estado = 'cerrado'
    deb.save()
    return redirect('index')

##@brief Funcion que guarda un nuevo debate, tambien lo edita
##@param request solicitud web
##@warning Login is required
@login_required
def crear_debate(request):
    if request.method == 'POST':
        ti = request.POST['titulo']
        des = request.POST['descripcion']
        largo_max = request.POST['largo_m']
        alias = request.POST['alias']
        fecha_fin = request.POST['date']
        if (fecha_fin):
            print(fecha_fin)
        else:
            fecha_fin= None
            print("null")
        print(fecha_fin)
        print("valor checkbox 'alias':")
        usuario = request.user
    try:
        id_deb=request.POST['id_debate_editar']
        publicar = Debate.objects.get(id_debate=id_deb,id_usuario_id=usuario)
        publicar.titulo=ti
        publicar.descripcion=des
        publicar.alias_c=alias
        publicar.date_fin=fecha_fin
        publicar.largo=largo_max

    except:
        publicar= Debate(titulo=ti, descripcion=des, id_usuario_id=usuario.id,
            largo=largo_max, alias_c=alias, date_fin= fecha_fin)
    publicar.save()
    

##@brief Funcion que actualiza el debate "cerrado" a "abierto"
##@param request solicitud web
##@return redirect redirecciona a la vista "perfil"
##@warning Login is required
@login_required
def republicar_debate(request):
    id_deb=request.POST['id_deb_republicar']
    deb = Debate.objects.get(pk=id_deb)
    ahora = datetime.date.today()
    if (deb.date_fin != None) and deb.date_fin <= ahora :
        deb.date_fin = None
    deb.estado = 'abierto'
    deb.save()
    return redirect('perfil')

##@brief Funcion que elimina un debate
##@param request solicitud web
##@return redirect redirecciona a la vista "perfil"
##@warning Login is required
@login_required
def eliminar_debate(request):
    id_deb=request.POST['id_deb_eliminar']
    deb = Debate.objects.get(pk=id_deb)
    deb.delete()
    return redirect('perfil')

##@brief Funcion que despliega los datos del usuario, debates abiertos, cerrados y opciones para cada uno.
##@param request solicitud web
##@return redirect redirecciona a la vista "perfil"
##@warning Login is required
@login_required
def perfil(request):
    if request.method == 'POST':
        if 'id_deb' in request.POST:
            cerrar_debate(request)
            return redirect('perfil')

        if 'nuevo_alias' in request.POST:
            nuevo_alias = request.POST['nuevo_alias']
            usuario = request.user
            print (usuario.id)
            publicar= Perfil.objects.get(user=usuario)
            publicar.alias = nuevo_alias
            publicar.save()
            return redirect('perfil')

        if 'id_debate_editar' in request.POST:
            crear_debate(request)
            return redirect('perfil')

        if 'id_deb_eliminar' in request.POST:
            eliminar_debate(request)
            
        if 'id_deb_republicar' in request.POST:
            republicar_debate(request)


    usuario = request.user
    alias_usuario = Perfil.objects.get(user=usuario)

    debates_abiertos = Debate.objects.filter(id_usuario_id= usuario.id, estado= 'abierto').order_by('-id_debate')
    debates_cerrados = Debate.objects.filter(id_usuario_id= usuario.id, estado= 'cerrado').order_by('-id_debate')
    lista_debates_abiertos = []

    for debate in debates_abiertos:
        num_posturas_debate = Postura.objects.filter(id_debate_id = debate.id_debate).count()
        if num_posturas_debate>0:
            puede_editar = "no"
        else: 
            puede_editar = "si"
        lista_debates_abiertos.append([debate, puede_editar])

    

    
    return render(request, 'perfil_usuario.html', {'usuario': usuario,
        'alias': alias_usuario,
        'debates_abiertos': lista_debates_abiertos,
        'debates_cerrados': debates_cerrados,
        })

