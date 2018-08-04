from django.shortcuts import render, render_to_response
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


from django.http import HttpResponse
from django.shortcuts import redirect
import requests

from django.http import HttpResponse
from resumen.models import Debate
from debate.models import Postura, Argumento, Respuesta, Valoracion, Edicion
from perfil.models import Perfil, Notificacion
from resumen.forms import creaDebateForm, LoginForm

def home(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        usuario = data.get("name_user")
        clave = data.get("password_user")
        acceso = authenticate(username=usuario, password=clave)
        if acceso is not None:
            login(request,acceso)
            return redirect('index')
        else:
            return redirect('home')
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request,"home.html", context)

##@brief Funcion que despliega todos los debates
##@param request solicitud web
##@return render redirecciona a "index.html" con la lista de todos los debates
##@warning Login is required
@login_required
def index(request):
    usuario = request.user
    iniciando_alias(request, usuario)
    creador=[('username', User.objects.get(id=request.user.id).username),
	         ('alias',Perfil.objects.get(user= request.user).alias)]
    form = creaDebateForm(creador=creador)
    if request.method == 'POST':
        if 'id_deb' in request.POST:
            cerrar_debate(request)
        # if 'descripcion' in request.POST:
        #     form = crear_debate(request)
        #     return redirect('index')



    category_list = Debate.objects.all().order_by('-id_debate')
    for debate in category_list:
        ahora = datetime.date.today()
        if debate.estado != 'cerrado' and debate.date_fin!= None and debate.date_fin <= ahora :
            debate.estado = 'cerrado'
            debate.save()
    print("el usuario activo es_: ", usuario.id)
    perfil_usuario = Perfil.objects.get(user_id= usuario.id)
    alias_usuario = perfil_usuario.alias
    notificaciones = Notificacion.objects.all()
    notificacion_usr = []
    for n in notificaciones:
        deb_usr=Debate.objects.get(id_debate = n.id_debate.id_debate).id_usuario
        if deb_usr == request.user:
            notificacion_usr.append(n)
    context = {'object_list': category_list, 'usuario': usuario, 'alias': alias_usuario,
                'form':form, 'notificaciones':notificacion_usr}
    return render(request, 'index.html', context)

##@brief Funcion que inicializa el alias del usuario actual, en caso de no tener alias sera "anonimo".
##@param request solicitud web
##@param u usuario a crear alias.
##@warning Login is required
@login_required
def iniciando_alias(request, u):
    try:
        usuario_2 = Perfil.objects.get(user= u)
        alias_usuario = usuario_2.alias
    except:
        perfil_usuario= Perfil(user=u)
        perfil_usuario.save()
        usuario_2 = Perfil.objects.get(user= u)
        alias_usuario = usuario_2.alias

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
    return redirect('index')

##@brief Funcion que guarda un nuevo debate
##@param request solicitud web
##@warning Login is required
@login_required
def crear_debate(request):
    if request.method == "POST":
            form = creaDebateForm(request.POST, request.FILES, creador=0)
            if form.is_valid():
                post = form.save(commit=False)
                post.id_usuario = request.user
                post.save()
    return form
