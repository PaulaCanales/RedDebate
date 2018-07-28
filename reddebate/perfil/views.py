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

# Create your views here.
##@brief Funcion que despliega los datos del usuario, debates abiertos, cerrados y opciones para cada uno.
##@param request solicitud web
##@return redirect redirecciona a la vista "perfil"
##@warning Login is required
@login_required
def perfiles(request, id):
    input  = id.split("X")
    if input[1]=="argumento":
        argumento = Argumento.objects.get(id_argumento=input[0])
        usa_alias = argumento.alias_c
        usuario = User.objects.get(id=argumento.id_usuario_id)
        alias_usuario = Perfil.objects.get(user_id=usuario)

    elif input[1]=="respuesta":
        respuesta = Respuesta.objects.get(id_respuesta=input[0])
        usa_alias = respuesta.alias_c
        usuario = User.objects.get(id=respuesta.id_usuario_id)
        alias_usuario = Perfil.objects.get(user_id=usuario)

    return render(request, 'perfiles.html', {'usuario': usuario,
        'alias': alias_usuario, 'usa_alias': usa_alias})



##@brief Funcion que despliega los datos del usuario, debates abiertos, cerrados y opciones para cada uno.
##@param request solicitud web
##@return redirect redirecciona a la vista "perfil"
##@warning Login is required
@login_required
def perfil(request):
    perfil= Perfil.objects.get(user=request.user)
    alias_form = modificaAlias(instance=perfil)
    if request.method == 'POST':
        if 'id_deb' in request.POST:
            cerrar_debate(request)
            return redirect('perfil')

        if 'nuevo_alias' in request.POST:
            alias_form = modificaAlias(request.POST, instance=perfil)
            if alias_form.is_valid():
                perfil = alias_form.save(commit=False)
                perfil.save()
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
        'alias_form': alias_form,
        })
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
