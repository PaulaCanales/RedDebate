# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from datetime import *
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
import unicodedata

# Create your models here.
class Debate(models.Model):
    #parametros de la tabla.
    id_debate = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    date = models.DateField(default=datetime.now, blank=True)
    date_fin = models.DateField(default=None, blank=True, null=True)
    alias_c = models.CharField(max_length=50, default='username')
    largo = models.IntegerField(default=300, blank=True)
    id_usuario = models.ForeignKey(User)
    estado = models.CharField(max_length=20, default='abierto')
    img = models.FileField(blank=True, null=True)
    num_argumento = models.IntegerField(default=1)
    num_cambio_postura = models.IntegerField(default=3)
    num_rebate = models.IntegerField(default=1)
    tipo_rebate = models.IntegerField(default=0) # 0:ambas # 1: contraria
    tipo_participacion = models.IntegerField(default=0) #0 debate publico

    tags = TaggableManager()

    def __unicode__(self): # __unicode__ on Python 2
		return self.titulo
    def __getitem__(self, key):
        return getattr(self, key)
    def as_dict(self):
        return {'titulo': self.titulo, 'tipo':self.tipo_participacion}
