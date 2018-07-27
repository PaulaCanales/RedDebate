"""reddebate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.views import logout as logout_social
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^resumen/', include('resumen.urls')),
    url(r'^debate/', include('debate.urls')),
    url(r'^perfil/', include('perfil.urls')),
    url(r'^admin/', admin.site.urls),


    #Python social auth
    url('social/', include('social.apps.django_app.urls', namespace='social')),
	# Home URL Fuente: "https://platzi.com/blog/login-redes-sociales-django/"
	url(r'^$', TemplateView.as_view(template_name="home.html"), name='social'),

    # Logout URL
    url( r'^users/logout/$',logout_social,
    {'next_page': '/reddebate'}, name="user-logout"),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
