from __future__ import unicode_literals
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from datetime import *
from django.db import models

# Create your models here.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    alias = models.CharField(max_length=30, default="anonimo")
#Como acceder al alias?
#u = User.objects.get(username='fsmith')
#alias_usuario = u.Usuario.alias
#class Usuario(models.Model):
#    parametros de la tabla. 
#    class UserProfile(models.Model):
#        id_usuario = models.ForeignKey(User)
#   id_usuario = models.AutoField(primary_key=True)
#   nombre = models.CharField(max_length=30)
#   alias = models.CharField(max_length=30)
#   def __unicode__(self): # __unicode__ on Python 2
#       return self.nombre


class Debate(models.Model):
    #parametros de la tabla. 
    id_debate = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    date = models.DateField(default=datetime.now, blank=True)
    date_fin = models.DateField(default=None, blank=True, null=True)
    alias_c = models.CharField(max_length=50, default='username')
    largo = models.IntegerField(default=300, blank=True)
    id_usuario = models.ForeignKey(User)
    estado = models.CharField(max_length=20, default='abierto')

    def __unicode__(self): # __unicode__ on Python 2
		return self.titulo


class Postura(models.Model):
    #parametros de la tabla. 
    id_postura = models.AutoField(primary_key=True)
    postura = models.IntegerField(default=1)
    date_Postura = models.DateField(default=datetime.now)
    id_usuario = models.ForeignKey(User)
    id_debate = models.ForeignKey(Debate)

    def __unicode__(self): # __unicode__ on Python 2
        return self.postura



class Argumento(models.Model):
    #parametros de la tabla. 
    id_argumento = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=300)
    postura = models.IntegerField(default=1)
    alias_c = models.CharField(max_length=50, default='username')
    date_argumento = models.DateField(default=datetime.now)
    id_usuario = models.ForeignKey(User)
    id_debate = models.ForeignKey(Debate)

    def __unicode__(self): # __unicode__ on Python 2
        return self.descripcion

class Respuesta(models.Model):
    #parametros de la tabla. 
    id_respuesta = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=300)
    alias_c = models.CharField(max_length=50, default='username')
    date_respuesta = models.DateField(default=datetime.now)
    id_usuario = models.ForeignKey(User)
    id_argumento = models.ForeignKey(Argumento)

    def __unicode__(self): # __unicode__ on Python 2
        return self.descripcion

class Valoracion(models.Model):
    #parametros de la tabla. 
    id_valoracion = models.AutoField(primary_key=True)
    date_valoracion = models.DateField(default=datetime.now)
    id_usuario = models.ForeignKey(User)
    id_argumento = models.ForeignKey(Argumento)
    

    def __unicode__(self): # __unicode__ on Python 2
        return self.id_valoracion

class Edicion(models.Model):
    #parametros de la tabla. 
    id_edicion = models.AutoField(primary_key=True)
    descripcion_edicion = models.CharField(max_length=300)
    date_edicion = models.DateField(default=datetime.now)
    id_argumento = models.ForeignKey(Argumento)
    

    def __unicode__(self): # __unicode__ on Python 2
        return self.descripcion_edicion
