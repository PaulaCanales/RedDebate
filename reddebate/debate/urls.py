from django.conf.urls import url, include

from . import views

# ex: /polls/5/
urlpatterns = [

	#url(r'^post_arg$', views.post_arg, name='post_arg'),
	url(r'^(?P<id_debate>[0-9]+)/$', views.showDebate, name='showDebate'),
	url(r'^(?P<id_debate>[0-9]+)/(?P<id_notification>[0-9]+)$', views.ver_notificacion, name='ver_notificacion'),
	url(r'^', include('resumen.urls', namespace='resumen'))

]
