from __future__ import unicode_literals
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from datetime import *
from django.db import models

from resumen.models import Debate
from perfil.models import Perfil


# Create your models here.

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
    date_edicion = models.DateTimeField(default=datetime.now)
    id_argumento = models.ForeignKey(Argumento)


    def __unicode__(self): # __unicode__ on Python 2
        return self.descripcion_edicion
