# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.views.generic import DetailView, ListView
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
from django.db.models import Q
from django.http import HttpResponse
from resumen.models import Debate
from debate.models import Postura, Argumento, Respuesta, Valoracion, Edicion, Participantes, Visita
from perfil.models import Perfil, Notificacion, Listado, UsuarioListado
from resumen.forms import newDebateForm, LoginForm
from taggit.models import Tag
from django.db.models import Q, Sum
from debate.views import updateReputation

def home(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect('index')
    context = {'form':form}
    return render(request,"home.html", context)

@login_required
def logout(request):
    django_logout(request)
    return redirect('home')

def closedIndex(request):
    actual_user = request.user
    startAlias(request, actual_user)
    creator=[('username', User.objects.get(id=request.user.id).username),
	         ('alias',Perfil.objects.get(user= request.user).alias)]
    total_users = User.objects.exclude(id=actual_user.id)
    actual_user_list = Listado.objects.filter(creador_id=actual_user.id).values()
    form = newDebateForm(creador=creator, usuarios=total_users, listado=actual_user_list)
    if request.method == 'GET':
        if 'q' in request.GET:
            deb = search(request)
            public_deb = 0
            private_deb = 0
            for d in deb:
                if(d.tipo_participacion == 0): public_deb+=1
                if(d.tipo_participacion == 1): private_deb+=1
            debates = debateData(deb, actual_user, False)
            label = "Resultados de la búsqueda: "+str(request.GET.get('q'))
            context = {'total_data_deb': debates, 'actual_user': actual_user, 'alias': Perfil.objects.get(user_id= actual_user.id).alias,
                        'form':form, 'label':label,
                        'public_deb': public_deb, 'private_deb': private_deb}
            return render(request, "filtro.html" , context)
    context = makeData(request, actual_user, form, 'cerrado')
    return render(request, "index.html", context)

##@brief Funcion que showDebate todos los debates
##@param request solicitud web
##@return render redirecciona a "index.html" con la lista de todos los debates
##@warning Login is required
@login_required
def index(request):
    actual_user = request.user
    startAlias(request, actual_user)
    creator=[('username', User.objects.get(id=request.user.id).username),
	         ('alias',Perfil.objects.get(user= request.user).alias)]
    total_users = User.objects.exclude(id=actual_user.id)
    actual_user_list = Listado.objects.filter(creador_id=actual_user.id).values()
    form = newDebateForm(creador=creator, usuarios=total_users, listado=actual_user_list)
    if request.method == 'POST':
        if 'id_deb' in request.POST:
            closeDebate(request)
            return redirect('index')

        if 'id_delete_deb' in request.POST:
            deleteDebate(request)
            return redirect('index')

    if request.method == 'GET':
        if 'q' in request.GET:
            deb = search(request)
            public_deb = 0
            private_deb = 0
            for d in deb:
                if(d.tipo_participacion == 0): public_deb+=1
                if(d.tipo_participacion == 1): private_deb+=1
            debates = debateData(deb, actual_user, False)
            moderator_view_deb = debateData(deb, actual_user, True)
            label = "Resultados de la búsqueda: "+str(request.GET.get('q'))
            context = {'total_data_deb': debates, 'actual_user': actual_user, 'alias': Perfil.objects.get(user_id= actual_user.id).alias,
                        'form':form,'label':label,
                        'deb_pub': public_deb, 'deb_pri': private_deb,
                        'moderator_view_deb':moderator_view_deb}
            return render(request, "filtro.html" , context)
    context = makeData(request, actual_user, form, 'abierto')
    return render(request, 'index.html', context)

def makeData(request, actual_user, form, state):
    total_debates = Debate.objects.all().order_by('-id_debate')
    total_data_deb = []
    #cierra debates expirados
    for debate in total_debates:
        ahora = datetime.date.today()
        if debate.estado != 'cerrado' and debate.date_fin!= None and debate.date_fin <= ahora :
            debate.estado = 'cerrado'
            debate.save()
    #obtener informacion de los debates dependiendo de su estado
    total_debates = Debate.objects.filter(estado=state).order_by('-id_debate')
    total_data_deb = debateData(total_debates,actual_user,False)
    moderator_view_deb = debateData(total_debates,actual_user,True)
    #debates populares por cantidad de posturas
    top_debates = sorted(total_data_deb, key=lambda k: k['position_num'], reverse=True)[:5]
    moderator_top_debates = sorted(moderator_view_deb, key=lambda k: k['position_num'], reverse=True)[:5]
    #perfil del usuario actual
    user_profile = Perfil.objects.get(user_id= actual_user.id)
    user_alias = user_profile.alias
    #obtener tags de los debates publicos
    tags_list = [tag.name for tag in Tag.objects.all()]
    public_debates = Debate.objects.filter(tipo_participacion=0)
    top_tags = Debate.tags.most_common(extra_filters={'debate__in': public_debates})[:5]
    #obtener usuarios populares por reputacion
    top_reputation = Perfil.objects.all().order_by('-reputacion')[:5]
    top_users = []
    for user in top_reputation:
        usr = User.objects.get(id=user.user_id)
        profile = Perfil.objects.get(user_id=user.user_id)
        top_users.append({'user':usr, 'profile':profile})
    #obtener debates recientes
    recent_debates = Debate.objects.filter(tipo_participacion=0).order_by('-id_debate')[:5]
    recent_data_deb = debateData(recent_debates,actual_user, False)
    moderator_recent_debates = Debate.objects.all().order_by('-id_debate')[:5]
    moderator_recent_data_deb = debateData(moderator_recent_debates,actual_user, True)
    #obtener listado del usuario actual
    actual_user_list = Listado.objects.filter(creador_id=actual_user.id).values()

    context = {'moderator_view_deb':moderator_view_deb, 'total_data_deb': total_data_deb, 'actual_user': actual_user, 'alias': user_alias,
                'form':form, 'top_tags':top_tags, 'top_deb':top_debates,
                'top_users':top_users, 'recent_data_deb': recent_data_deb, 'moderator_recent_deb': moderator_recent_data_deb,
                'moderator_top_deb': moderator_top_debates, 'actual_user_list':actual_user_list}
    return context

def debateData(debates, user, moderator):
    debate_list = []
    for debate in debates:
        infavor_position_num = Postura.objects.filter(id_debate_id=debate.id_debate, postura=1).count()
        against_position_num = Postura.objects.filter(id_debate_id=debate.id_debate, postura=0).count()
        argument_num = Argumento.objects.filter(id_debate_id=debate.id_debate).count()
        position_num = infavor_position_num + against_position_num
        visits = Visita.objects.filter(id_debate=debate).aggregate(Sum('num')).values()[0]
        if not visits: visits=0
    	if (int(position_num)==0):
            against_percent=0
            infavor_percent=0
    	else:
            infavor_percent = (float(infavor_position_num) / float(position_num))*100
            against_percent = (float(against_position_num) / float(position_num))*100
        if debate.tipo_participacion == 1 and not moderator:
            try:
                participate = Participantes.objects.get(id_debate_id=debate.id_debate, id_usuario_id=user.id)
                debate_list.append({"datos":debate, "infavor_percent":infavor_percent, "against_percent":against_percent,
                                        "infavor_position_num":infavor_position_num, "against_position_num":against_position_num,
                                        "position_num":position_num, "arg_num":argument_num,
                                        "visits": visits})

            except:
                participate = False
        else:
            debate_list.append({"datos":debate, "infavor_percent":infavor_percent, "against_percent":against_percent,
                                    "infavor_position_num":infavor_position_num, "against_position_num":against_position_num,
                                    "position_num":position_num, "arg_num":argument_num,
                                    "visits": visits})
    return debate_list

def tagged(request, slug):
    actual_user = request.user
    user_profile = Perfil.objects.get(user_id= actual_user.id)
    total_users = User.objects.exclude(id=actual_user.id)
    creator=[('username', User.objects.get(id=request.user.id).username),
	         ('alias',user_profile.alias)]
    actual_user_list = Listado.objects.filter(creador_id=actual_user.id).values()
    form = newDebateForm(creador=creator, usuarios=total_users, listado=actual_user_list)
    debate_list = Debate.objects.filter(tags__slug=slug)
    total_data_deb = debateData(debate_list, actual_user, False)
    moderator_view_deb = debateData(debate_list, actual_user, True)
    top_tags = Debate.tags.most_common()[:5]
    label = "Tags relacionados: "+slug
    context = {'total_data_deb':total_data_deb, 'usuario': actual_user, 'alias': user_profile.alias,
                 'form':form, 'top_tags':top_tags, 'label':label, 'moderator_view_deb':moderator_view_deb}

    return render(request, 'filtro.html', context)

##@brief Funcion que inicializa el alias del usuario actual, en caso de no tener alias sera "anonimo".
##@param request solicitud web
##@param u usuario a crear alias.
##@warning Login is required
@login_required
def startAlias(request, u):
    try:
        user = Perfil.objects.get(user= u)
        user_alias = user.alias
    except:
        user_profile= Perfil(user=u)
        user_profile.save()
        user = Perfil.objects.get(user= u)
        user_alias = user.alias

##@brief Funcion que cierra el debate
##@param request solicitud web
##@return redirect redirecciona a la vista "index"
##@warning Login is required
@login_required
def closeDebate(request):
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
def deleteDebate(request):
    id_deb=request.POST['id_delete_deb']
    deb = Debate.objects.get(pk=id_deb)
    deb.delete()
    updateReputation(request.user.id, -5)
    return redirect('debates')

def search(request):
    query = request.GET.get('q')
    results = Debate.objects.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query))
    return results
