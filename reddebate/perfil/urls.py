from django.conf.urls import url

from . import views

# ex: /polls/5/
urlpatterns = [

	#url(r'^post_arg$', views.post_arg, name='post_arg'),
	#url(r'^(?P<id_debate>[0-9]+)/$', views.despliega, name='despliega'),
    url(r'^perfil/$', views.perfil, name='perfil'),
    url(r'^(?P<id_argumento>[0-9]+)/$', views.perfiles, name='perfiles')

]
