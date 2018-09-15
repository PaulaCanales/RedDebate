from django.conf.urls import url, include

from . import views

# ex: /polls/5/
urlpatterns = [

	#url(r'^post_arg$', views.post_arg, name='post_arg'),
	#url(r'^(?P<id_debate>[0-9]+)/$', views.despliega, name='despliega'),
    url(r'^(?P<id_usr>[0-9]+)/$', views.perfil, name='perfil'),
    url(r'^usr/(?P<id_arg>[0-9]+)/$', views.perfil, name='perfil'),
    url(r'^usr/(?P<id_arg>[0-9]+)/(?P<id_reb>[0-9]+)/$', views.perfil, name='perfil'),
    url(r'^debates$', views.debates_usuario, name='debates'),
    url(r'^lista/(?P<id_lista>[0-9]+)/$', views.lista, name='lista'),
    url(r'^', include('resumen.urls', namespace='resumen'))
]
