from __future__ import unicode_literals
from django.db.models.fields.related import ForeignKey
from datetime import *
from django.db import models

# Create your models here.

class Usuario(models.Model):
    #parametros de la tabla. 
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)

    def __unicode__(self): # __unicode__ on Python 2
		return self.nombre


class Debate(models.Model):
    #parametros de la tabla. 
    id_debate = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    date = models.DateField(default=datetime.now, blank=True)
    id_usuario= models.ForeignKey(Usuario)
    estado= models.CharField(max_length=20, default='abierto')

    def __unicode__(self): # __unicode__ on Python 2
		return self.titulo




    



