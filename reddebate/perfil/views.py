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
from perfil.models import Perfil
from debate.models import Postura, Argumento, Respuesta
from perfil.forms import modificaAlias
from resumen.views import verificaNotificacion, datos_debates
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
                if 'id_deb' in request.POST:
                    cerrar_debate(request)
                    return redirect('perfil',id_usr=request.user.id)

                if 'nuevo_alias' in request.POST:
                    alias_form = modificaAlias(request.POST, instance=perfil)
                    if alias_form.is_valid():
                        perfil = alias_form.save(commit=False)
                        perfil.save()
                        return redirect('perfil',id_usr=request.user.id)

                if 'id_debate_editar' in request.POST:
                    crear_debate(request)
                    return redirect('perfil',id_usr=request.user.id)

                if 'id_deb_eliminar' in request.POST:
                    eliminar_debate(request)

                if 'id_deb_republicar' in request.POST:
                    republicar_debate(request)


            usuario = request.user
            alias_usuario = Perfil.objects.get(user=usuario)
            debates_usuario = Debate.objects.filter(id_usuario_id= usuario.id).order_by('-id_debate')
            lista_debates = datos_debates(debates_usuario,usuario)

            stats = estadisticas_usuario(usuario.id)
            notificacion_usr = verificaNotificacion(request)
            return render(request, 'perfil_usuario.html', {'usuario': usuario,
                'alias': alias_usuario,
                'object_list': lista_debates,
                'alias_form': alias_form, 'notificaciones': notificacion_usr,
                'stats': stats
                })
        else:
            usa_alias = 'username'
            usuario = User.objects.get(id=id_usr)
            alias_usuario = Perfil.objects.get(user_id=usuario)
            stats = estadisticas_usuario(usuario.id)
            total_usuarios = User.objects.all()
            notificacion_usr = verificaNotificacion(request)
            return render(request, 'perfiles.html', {'usuario': usuario,
                'alias': alias_usuario, 'usa_alias': usa_alias, 'total_usuarios': total_usuarios,
                'notificaciones': notificacion_usr, 'stats': stats})

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
        notificacion_usr = verificaNotificacion(request)
        return render(request, 'perfiles.html', {'usuario': usuario,
            'alias': alias_usuario, 'usa_alias': usa_alias, 'total_usuarios': total_usuarios,
            'notificaciones': notificacion_usr, 'stats': stats})


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

##@brief Funcion que cierra el debate
##@param request solicitud web
##@return redirect redirecciona a la vista "index"
##@warning Login is required
@login_required
def cerrar_debate(request):
    id_deb = request.POST['id_deb']
    deb = Debate.objects.get(pk=id_deb)
    deb.estado = 'cerrado'
    deb.save()
    return redirect('perfil',id_usr=request.user.id)

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
    return redirect('perfil',id_usr=request.user.id)
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
    return redirect('perfil',id_usr=request.user.id)
