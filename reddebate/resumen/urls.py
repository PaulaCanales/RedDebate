from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^resumen/', views.index, name='index'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^post/new/$', views.crear_debate, name='post_new'),

    #url(r'^perfil/$', views.perfil, name='perfil'),
    #url(r'^(?P<id_argumento>[0-9]+)/$', views.perfiles, name='perfiles')
    #url(r'^debate', views.despliega, name='despliega'),


    #url(r'^(?P<id_debate>[0-9]+)/$', views.despliega, name='despliega'),
    #url(r'^debate/(?P<id_deb>[0-9]+)/$', views.despliega, name='despliega'),
    #url: "/debate/"+(configs[id-1]["id_deb"].toString()).concat("/")
]
