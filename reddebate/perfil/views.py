from django.shortcuts import render, render_to_response
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
from django.shortcuts import redirect
import requests
from collections import Counter
import math

from django.http import HttpResponse
from resumen.models import Debate
from perfil.models import Perfil, Listado, UsuarioListado
from debate.models import Postura, Argumento, Respuesta
from perfil.forms import modificaAlias, creaListado, seleccionaUsuarios, seleccionaListados, modificaImagen
from resumen.views import debateData, closeDebate
from debate.views import updateReputation

##@brief Funcion que despliega los datos del usuario, debates abiertos, cerrados y opciones para cada uno.
##@param request solicitud web
##@return redirect redirecciona a la vista "perfil"
##@warning Login is required
@login_required
def perfil(request, id_usr=None, id_arg=None, id_reb=None):
    if id_usr!=None:
        if int(request.user.id)==int(id_usr):
            perfil= Perfil.objects.get(user=request.user)
            alias_form = modificaAlias(instance=perfil)

            if request.method == 'POST':
                if 'nuevo_alias' in request.POST:
                    alias_form = modificaAlias(request.POST, instance=perfil)
                    if alias_form.is_valid():
                        perfil = alias_form.save(commit=False)
                        perfil.save()
                        return redirect('perfil',id_usr=request.user.id)
                elif 'nueva_imagen' in request.POST:
                    form = modificaImagen(request.POST, request.FILES)
                    if form.is_valid():
                        post = Perfil.objects.get(user=request.user)
                        post.img = form.cleaned_data['img']
                        post.save()
                        return redirect('perfil',id_usr=request.user.id)
            usuario = request.user
            user_alias = Perfil.objects.get(user=usuario)
            imagen_form = modificaImagen()
            stats = estadisticas_usuario(usuario.id)
            return render(request, 'user_profile.html', {'usuario': usuario,
                'alias': user_alias, 'alias_form': alias_form,
                'stats': stats, 'imagen_form':imagen_form})
        else:
            usa_alias = 'username'
            usuario = User.objects.get(id=id_usr)
            user_alias = Perfil.objects.get(user_id=usuario)
            stats = estadisticas_usuario(usuario.id)
            total_usuarios = User.objects.all()
            listas_de_usuario = UsuarioListado.objects.filter(usuario_id = usuario.id)
            listas = Listado.objects.filter(creador_id=request.user.id)
            listas_disponibles = listas.exclude(id__in=listas_de_usuario.values('lista_id')).values()
            listas_no_disponibles = listas.filter(id__in=listas_de_usuario.values('lista_id')).values()
            form = seleccionaListados(listas=listas_disponibles, usuario=usuario.id)
            if request.method == 'POST':
                if 'nuevoUsrLista' in request.POST:
                    usr = request.POST['usuario']
                    seleccion = request.POST.getlist('lista_id')
                    if (len(seleccion)>0):
                        for lista in seleccion:
                            post = UsuarioListado(usuario_id=usr, lista_id=lista)
                            post.save()
                    if request.POST['nueva']:
                        nombre = request.POST['nueva']
                        nueva_lista = Listado(nombre=nombre, creador_id=request.user.id)
                        nueva_lista.save()
                        nuevo_usr = UsuarioListado(usuario_id=usr, lista_id=nueva_lista.id)
                        nuevo_usr.save()
                    return redirect('perfil', id_usr=usr)

            return render(request, 'perfiles.html', {'usuario': usuario,
                'alias': user_alias, 'usa_alias': usa_alias, 'total_usuarios': total_usuarios,
                'stats': stats, 'form':form, 'listas_de_usuario':listas_no_disponibles})

    else:
        if id_reb!=None:
            respuesta = Respuesta.objects.get(id_respuesta=id_reb)
            usa_alias = respuesta.alias_c
            usuario = User.objects.get(id=respuesta.id_usuario_id)
            user_alias = Perfil.objects.get(user_id=usuario)
        else:
            argumento = Argumento.objects.get(id_argumento=id_arg)
            usa_alias = argumento.alias_c
            usuario = User.objects.get(id=argumento.id_usuario_id)
            user_alias = Perfil.objects.get(user_id=usuario)
        stats = estadisticas_usuario(usuario.id)
        total_usuarios = User.objects.all()
        listas_de_usuario = UsuarioListado.objects.filter(usuario_id = usuario.id)
        listas = Listado.objects.filter(creador_id=request.user.id)
        listas_disponibles = listas.exclude(id__in=listas_de_usuario.values('lista_id')).values()
        listas_no_disponibles = listas.filter(id__in=listas_de_usuario.values('lista_id')).values()
        form = seleccionaListados(listas=listas_disponibles, usuario=usuario.id)
        return render(request, 'perfiles.html', {'usuario': usuario,
            'alias': user_alias, 'usa_alias': usa_alias, 'total_usuarios': total_usuarios,
            'stats': stats, 'form':form, 'listas_de_usuario':listas_no_disponibles})


def estadisticas_usuario(id_usuario):
    debates = Debate.objects.all().order_by('-id_debate')
    debates_usr = Debate.objects.filter(id_usuario_id= id_usuario)
    participaciones = Postura.objects.filter(id_usuario_id=id_usuario).values('id_debate_id')
    participaciones_deb = Debate.objects.filter(id_debate__in=participaciones)
    tags = find_tags(debates_usr, participaciones_deb)
    num_debates_usr = Debate.objects.filter(id_usuario_id= id_usuario).count()
    num_posturas_usr = Postura.objects.filter(id_usuario_id = id_usuario).count()
    num_argumentos_usr = Argumento.objects.filter(id_usuario_id = id_usuario).count()
    num_rebates_usr = Respuesta.objects.filter(id_usuario_id = id_usuario).count()
    triunfos = 0
    derrotas = 0
    mejor_arg = 0
    peor_arg = 0
    for debate in debates:
        try:
            postura_usr = Postura.objects.get(id_debate_id=debate.id_debate, id_usuario_id=id_usuario).postura
        except:
            postura_usr = "vacia"
        if (debate.estado == "cerrado"):
            infavor_position_num = Postura.objects.filter(id_debate_id=debate.id_debate, postura=1).count()
            against_position_num = Postura.objects.filter(id_debate_id=debate.id_debate, postura=0).count()
            argumentos = Argumento.objects.filter(id_debate_id=debate.id_debate).order_by('-puntaje')
            if len(argumentos)!=0:
                mejor_argumento = argumentos[0]
                peor_argumento = argumentos[len(argumentos)-1]
                if mejor_argumento.id_usuario.id == id_usuario:
                    mejor_arg += 1
                if peor_argumento.id_usuario.id == id_usuario:
                    peor_arg += 1

            if infavor_position_num>=against_position_num:
                postura_ganadora = 1
                postura_perdedora = 0
            else:
                postura_ganadora = 0
                postura_perdedora = 1

            if postura_ganadora == postura_usr:
                triunfos += 1
            if postura_perdedora == postura_usr:
                derrotas += 1
    stats = {'debates': num_debates_usr, 'posturas':num_posturas_usr,
             'argumentos': num_argumentos_usr, 'rebates':num_rebates_usr,
             'triunfos': triunfos, 'derrotas':derrotas,
             'mejor_arg':mejor_arg, 'peor_arg':peor_arg,
             'tags':tags}
    return stats

def debates_usuario(request):
    if request.method == 'POST':
        if 'id_deb' in request.POST:
            closeDebate(request)
            return redirect('debates')

        if 'id_delete_deb' in request.POST:
            deleteDebate(request)

        if 'id_deb_republicar' in request.POST:
            republicar_debate(request)
    usuario = request.user
    debates_usuario = Debate.objects.filter(id_usuario_id= usuario.id).order_by('-id_debate')
    lista_debates = debateData(debates_usuario,usuario,False)
    return render(request, 'debates_usuario.html', {'usuario': usuario, 'total_data_deb': lista_debates})

def find_tags(debate, participaciones):
    tags_usr = []
    for deb in debate:
        tags = deb.tags.all().values()
        for tag in tags:
            tags_usr.append(tag['name'])
    for deb in participaciones:
        tags = deb.tags.all().values()
        for tag in tags:
            tags_usr.append(tag['name'])
    tags_dict = dict(Counter(tags_usr))
    keys = [item.strip() for item in tags_dict.keys()]
    size = tags_dict.values()
    norm_size = [float(i)/max(size) * 10 for i in size]
    norm_size = [int(math.ceil(i)) for i in norm_size]
    dictionary = dict(zip(keys,norm_size))
    return dictionary

def listas_usuario(request):
    actual_user_list = Listado.objects.filter(creador=request.user).values()
    listado_usuarios = []
    total_data_deb = []
    for item in actual_user_list:
        usr_lista = UsuarioListado.objects.filter(lista_id=item['id']).values()
        for user in usr_lista:
            username = User.objects.get(id=user['usuario_id'])
            listado_usuarios.append({'nombre':username, 'lista_id':user['lista_id']})
    lista_form = creaListado()
    if request.method == 'POST':
        if 'nombre' in request.POST:
            lista_form = creaListado(request.POST)
            if lista_form.is_valid():
                lista = lista_form.save(commit=False)
                lista.creador = request.user
                lista.save()
                return redirect('lista', lista.id)
        if 'id_lista' in request.POST:
            id_lista = request.POST['id_lista']
            usuarioLista = Listado.objects.get(id=id_lista)
            usuarioLista.delete()
            return redirect('listas_usuario')

    return render(request, 'listas_usuario.html', {'usuario':request.user, 'actual_user_list': actual_user_list, 'lista_form': lista_form,
                'listado_usuarios': listado_usuarios})

def lista(request, id_lista):
    lista = Listado.objects.get(id=id_lista)
    usuarios = UsuarioListado.objects.filter(lista_id=id_lista)
    # perfiles = Perfil.objects.filter(user_id=usuarios.values('usuario_id'))
    usuario_perfil = []
    for usuario in usuarios:
        perfil = Perfil.objects.get(user_id=usuario.usuario_id)
        usuario_perfil.append({'usuario':usuario, 'perfil':perfil})
    excluir = [request.user.id]
    for item in usuarios:
        excluir.append(item.usuario_id)
    total_usuarios = User.objects.exclude(id__in=excluir)
    usrlista_form = seleccionaUsuarios(usuarios=total_usuarios, lista=id_lista)

    if request.method == 'POST':
        if 'usuario' in request.POST:
            seleccion = request.POST.getlist('usuario')
            for usr in seleccion:
                post = UsuarioListado(usuario_id=usr, lista_id=request.POST['lista_id'])
                post.save()
            return redirect('lista', request.POST['lista_id'])
        if 'id_usr_lista' in request.POST:
            id_usr = request.POST['id_usr_lista']
            id_lista = request.POST['id_lista']
            usuarioLista = UsuarioListado.objects.get(lista_id=id_lista, usuario_id=id_usr)
            usuarioLista.delete()
            return redirect('lista', id_lista)
    return render(request, 'lista.html', {'lista': lista, 'usuarios': usuario_perfil, 'form': usrlista_form})

##@brief Funcion que actualiza el debate "cerrado" a "abierto"
##@param request solicitud web
##@return redirect redirecciona a la vista "perfil"
##@warning Login is required
@login_required
def republicar_debate(request):
    id_deb=request.POST['id_deb_republicar']
    opc=request.POST['tab']
    deb = Debate.objects.get(pk=id_deb)
    if opc == "NULL":
        deb.date_fin = None
    else:
        yyyy,mm,dd=str(request.POST['nuevafecha']).split("-")
        deb.date_fin = datetime.date(int(yyyy),int(mm),int(dd))
    deb.estado = 'abierto'
    deb.save()
    return redirect('debates')
