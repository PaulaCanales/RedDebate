from __future__ import unicode_literals
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from datetime import *
from django.db import models
from django import forms

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

    def __unicode__(self): # __unicode__ on Python 2
		return self.titulo

class crearDebateForm(forms.Form):
    titulo = forms.CharField()
    descripcion = forms.CharField()
    largo_m = forms.IntegerField()
    alias = forms.CharField()
    date = forms.DateField(required=False)
    image = forms.FileField(required=False)
    id_usuario = forms.IntegerField()
