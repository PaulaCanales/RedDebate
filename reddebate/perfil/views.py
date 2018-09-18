from django.shortcuts import render, render_to_response
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
from django.shortcuts import redirect
import requests

from django.http import HttpResponse
from resumen.models import Debate
from perfil.models import Perfil, Listado, UsuarioListado
from debate.models import Postura, Argumento, Respuesta
from perfil.forms import modificaAlias, creaListado, seleccionaUsuarios, seleccionaListados
from resumen.views import datos_debates, cerrar_debate
from debate.views import actualiza_reputacion

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
            usuario = request.user
            alias_usuario = Perfil.objects.get(user=usuario)

            stats = estadisticas_usuario(usuario.id)
            return render(request, 'perfil_usuario.html', {'usuario': usuario,
                'alias': alias_usuario, 'alias_form': alias_form,
                'stats': stats})
        else:
            usa_alias = 'username'
            usuario = User.objects.get(id=id_usr)
            alias_usuario = Perfil.objects.get(user_id=usuario)
            stats = estadisticas_usuario(usuario.id)
            total_usuarios = User.objects.all()
            listas_de_usuario = UsuarioListado.objects.filter(usuario_id = usuario.id)
            listas = Listado.objects.filter(creador_id=request.user.id)
            listas = listas.exclude(id__in=listas_de_usuario.values('lista_id')).values()
            nombre_listas_de_usuario = Listado.objects.filter(id__in=listas_de_usuario.values('lista_id')).values()
            form = seleccionaListados(listas=listas, usuario=usuario.id)
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
                'alias': alias_usuario, 'usa_alias': usa_alias, 'total_usuarios': total_usuarios,
                'stats': stats, 'form':form, 'listas_de_usuario':nombre_listas_de_usuario})

    else:
        if id_reb!=None:
            respuesta = Respuesta.objects.get(id_respuesta=id_reb)
            usa_alias = respuesta.alias_c
            usuario = User.objects.get(id=respuesta.id_usuario_id)
            alias_usuario = Perfil.objects.get(user_id=usuario)
        else:
            argumento = Argumento.objects.get(id_argumento=id_arg)
            usa_alias = argumento.alias_c
            usuario = User.objects.get(id=argumento.id_usuario_id)
            alias_usuario = Perfil.objects.get(user_id=usuario)
        stats = estadisticas_usuario(usuario.id)
        total_usuarios = User.objects.all()
        return render(request, 'perfiles.html', {'usuario': usuario,
            'alias': alias_usuario, 'usa_alias': usa_alias, 'total_usuarios': total_usuarios,
            'stats': stat})


def estadisticas_usuario(id_usuario):
    debates = Debate.objects.all().order_by('-id_debate')
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
            num_posturas_af = Postura.objects.filter(id_debate_id=debate.id_debate, postura=1).count()
            num_posturas_ec = Postura.objects.filter(id_debate_id=debate.id_debate, postura=0).count()
            argumentos = Argumento.objects.filter(id_debate_id=debate.id_debate).order_by('-puntaje')
            if len(argumentos)!=0:
                mejor_argumento = argumentos[0]
                peor_argumento = argumentos[len(argumentos)-1]
                if mejor_argumento.id_usuario.id == id_usuario:
                    mejor_arg += 1
                if peor_argumento.id_usuario.id == id_usuario:
                    peor_arg += 1

            if num_posturas_af>=num_posturas_ec:
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
             'mejor_arg':mejor_arg, 'peor_arg':peor_arg}
    return stats

def debates_usuario(request):
    if request.method == 'POST':
        if 'id_deb' in request.POST:
            cerrar_debate(request)
            return redirect('debates')
        if 'id_debate_editar' in request.POST:
            crear_debate(request)
            return redirect('debates')

        if 'id_deb_eliminar' in request.POST:
            eliminar_debate(request)

        if 'id_deb_republicar' in request.POST:
            republicar_debate(request)
    usuario = request.user
    debates_usuario = Debate.objects.filter(id_usuario_id= usuario.id).order_by('-id_debate')
    lista_debates = datos_debates(debates_usuario,usuario)
    return render(request, 'debates_usuario.html', {'usuario': usuario, 'object_list': lista_debates})

def listas_usuario(request):
    listado = Listado.objects.filter(creador=request.user).values()
    listado_usuarios = []
    object_list = []
    for item in listado:
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

    return render(request, 'listas_usuario.html', {'usuario':request.user, 'listado': listado, 'lista_form': lista_form,
                'listado_usuarios': listado_usuarios})

def lista(request, id_lista):
    lista = Listado.objects.get(id=id_lista)
    usuarios = UsuarioListado.objects.filter(lista_id=id_lista)
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
    return render(request, 'lista.html', {'lista': lista, 'usuarios': usuarios, 'form': usrlista_form})

##@brief Funcion que elimina un debate
##@param request solicitud web
##@return redirect redirecciona a la vista "perfil"
##@warning Login is required
@login_required
def eliminar_debate(request):
    id_deb=request.POST['id_deb_eliminar']
    deb = Debate.objects.get(pk=id_deb)
    deb.delete()
    actualiza_reputacion(request.user.id, -5)
    return redirect('debates')
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
