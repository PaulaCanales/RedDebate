from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from social.apps.django_app.default.models import UserSocialAuth
 
'''Login por redes sociales
PARAMETROS: backend - Desde donde me estoy logueando
 strategy -
 details - Retorna username, nombre, apellido
 response - Información del perfil
 user - objeto del usuario logueado
'''
def login(backend, strategy, details, response, user=None, *args, **kwargs):
 
  try:
    #Obtengo el id social por luego obtener el iduser
    id_social = response['id']
 
    User = get_user_model()
 
    #Obtengo el user id
    aus = UserSocialAuth.objects.get(uid=id_social)
    iduser = aus.user_id
 
    #Verifico si ya no existe el usuario, solamente lo crea si no existe
    us = User.objects.filter(id=iduser)
    if us.count() == 0:
        #Verifico que tipo de backend es y obtengo el nombre de usuario
        if backend.name == 'facebook':
           surname = response["last_name"]
           name = response['first_name']
        elif backend.name == 'twitter':
           surname = response['name']
           name = ""
        else:
           return HttpResponseRedirect(reverse('url_de_logueo'))
 
        #Seteo que el usuario es del tipo usuario
        User.objects.filter(id=iduser).update(surname=surname,name=name)
  except Exception:
    return HttpResponseRedirect(reverse('url_de_logueo'))
