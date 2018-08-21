from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.views.generic import DetailView, ListView
from taggit.models import Tag
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
from django.http import HttpResponse
from resumen.models import Debate
from debate.models import Postura, Argumento, Respuesta, Valoracion, Edicion, Participantes
from perfil.models import Perfil, Notificacion
from resumen.forms import creaDebateForm, LoginForm
from taggit.models import Tag

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
    total_usuarios = User.objects.exclude(id=usuario.id)
    form = creaDebateForm(creador=creador, usuarios=total_usuarios)
    if request.method == 'POST':
        if 'id_deb' in request.POST:
            cerrar_debate(request)

    category_list = Debate.objects.all().order_by('-id_debate')
    object_list = []
    for debate in category_list:
        ahora = datetime.date.today()
        if debate.estado != 'cerrado' and debate.date_fin!= None and debate.date_fin <= ahora :
            debate.estado = 'cerrado'
            debate.save()
    object_list = datos_debates(category_list,usuario)
    top_debates = sorted(object_list, key=lambda k: k['num_posturas'], reverse=True)[:5]
    print("top_debates")
    print(top_debates)
    print("el usuario activo es: ", usuario.id)
    num_publico_abierto = Debate.objects.filter(estado='abierto', tipo_participacion=0).count()
    num_publico_cerrado = Debate.objects.filter(estado='cerrado', tipo_participacion=0).count()
    num_privado_abierto = Debate.objects.filter(estado='abierto', tipo_participacion=1, id_usuario=usuario).count()
    num_privado_cerrado = Debate.objects.filter(estado='cerrado', tipo_participacion=1, id_usuario=usuario).count()

    perfil_usuario = Perfil.objects.get(user_id= usuario.id)
    alias_usuario = perfil_usuario.alias
    notificacion_usr = verificaNotificacion(request)
    tags_list = [tag.name for tag in Tag.objects.all()]
    top_tags = Debate.tags.most_common()[:5]
    context = {'category_list':category_list, 'object_list': object_list, 'usuario': usuario, 'alias': alias_usuario,
                'form':form, 'notificaciones':notificacion_usr, 'top_tags':top_tags, 'top_deb':top_debates,
                'publico_abierto':num_publico_abierto, 'publico_cerrado':num_publico_cerrado,
                'privado_abierto':num_privado_abierto, 'privado_cerrado':num_privado_cerrado,}
    return render(request, 'index.html', context)

def datos_debates(debates, usuario):
    lista_debates = []
    for debate in debates:
        num_posturas_af = Postura.objects.filter(id_debate_id=debate.id_debate, postura=1).count()
        num_posturas_ec = Postura.objects.filter(id_debate_id=debate.id_debate, postura=0).count()
        num_posturas = num_posturas_af + num_posturas_ec
    	if (int(num_posturas)==0):
            puede_editar = "si"
            porcentaje_c=0
            porcentaje_f=0
    	else:
            puede_editar = "no"
            porcentaje_f = (float(num_posturas_af) / float(num_posturas))*100
            porcentaje_c = (float(num_posturas_ec) / float(num_posturas))*100
        if debate.tipo_participacion == 1:
            try:
                participa = Participantes.objects.get(id_debate_id=debate.id_debate, id_usuario_id=usuario.id)
                lista_debates.append({"datos":debate, "porcentaje_f":porcentaje_f, "porcentaje_c":porcentaje_c,
                                        "num_posturas_af":num_posturas_af, "num_posturas_ec":num_posturas_ec, "num_posturas":num_posturas})

            except:
                participa = False
        else:
            lista_debates.append({"datos":debate, "porcentaje_f":porcentaje_f, "porcentaje_c":porcentaje_c,
                                    "num_posturas_af":num_posturas_af, "num_posturas_ec":num_posturas_ec, "num_posturas":num_posturas})
    return lista_debates

def tagged(request, slug):
    usuario = request.user
    perfil_usuario = Perfil.objects.get(user_id= usuario.id)
    notificacion_usr = verificaNotificacion(request)
    total_usuarios = User.objects.exclude(id=usuario.id)
    creador=[('username', User.objects.get(id=request.user.id).username),
	         ('alias',perfil_usuario.alias)]
    form = creaDebateForm(creador=creador, usuarios=total_usuarios)
    debate_list = Debate.objects.filter(tags__slug=slug)
    object_list = datos_debates(debate_list, usuario)
    top_tags = Debate.tags.most_common()[:5]
    context = {'object_list':object_list, 'usuario': usuario, 'alias': perfil_usuario.alias,
                 'form':form, 'notificaciones':notificacion_usr, 'top_tags':top_tags}
    # context = {'object_list':object_list}
    return render(request, 'index.html', context)

@login_required
def verificaNotificacion(request):
    notificaciones = Notificacion.objects.all()
    notificacion_usr = []
    for n in notificaciones:
        deb_usr=Debate.objects.get(id_debate = n.id_debate.id_debate).id_usuario
        if deb_usr == request.user:
            notificacion_usr.append(n)
    return notificacion_usr

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
