from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^$', views.index, name='index'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    #url(r'^debate', views.despliega, name='despliega'),

    #url(r'^(?P<id_debate>[0-9]+)/$', views.despliega, name='despliega'),
    #url(r'^debate/(?P<id_deb>[0-9]+)/$', views.despliega, name='despliega'),
    #url: "/debate/"+(configs[id-1]["id_deb"].toString()).concat("/")
]


