from django.conf.urls import url, include

from . import views

# ex: /polls/5/
urlpatterns = [

	#url(r'^post_arg$', views.post_arg, name='post_arg'),
	#url(r'^(?P<id_debate>[0-9]+)/$', views.despliega, name='despliega'),
    url(r'^perfil/$', views.perfil, name='perfil'),
    url(r'^(?P<id>\w+)/$', views.perfiles, name='perfiles'),
    url(r'^', include('resumen.urls', namespace='resumen'))
]
