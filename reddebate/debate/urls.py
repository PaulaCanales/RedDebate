from django.conf.urls import url

from . import views

# ex: /polls/5/
urlpatterns = [

	#url(r'^post_arg$', views.post_arg, name='post_arg'),
	url(r'^(?P<id_debate>[0-9]+)/$', views.despliega, name='despliega'),

]
