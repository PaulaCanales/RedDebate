from __future__ import unicode_literals
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from datetime import *
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from resumen.models import Debate
from perfil.models import Perfil, Notificacion
from channels import Group

# Create your models here.

class Postura(models.Model):
    #parametros de la tabla.
    id_postura = models.AutoField(primary_key=True)
    postura = models.IntegerField(default=1)
    postura_inicial = models.IntegerField(default=1)
    cambio_postura = models.IntegerField(default=0)
    date_Postura = models.DateField(default=datetime.now)
    id_usuario = models.ForeignKey(User)
    id_debate = models.ForeignKey(Debate)

    def __unicode__(self): # __unicode__ on Python 2
        return self.postura
    def __getitem__(self, key):
        return getattr(self, key)
    def as_dict(self):
        # id_creador = Debate.objects.get(id_debate=self.id_debate.id_debate).id_usuario_id
        postura_f=Postura.objects.filter(id_debate_id=self.id_debate, postura=1).count()
        postura_c=Postura.objects.filter(id_debate_id=self.id_debate, postura=0).count()
        if (int(postura_f+postura_c)==0):
            porcentaje_f=0
            porcentaje_c=0
        else:
            porcentaje_f=round(float(postura_f) / float(postura_c+postura_f),3)*100
            porcentaje_c=round(float(postura_c) / float(postura_c+postura_f),3)*100
        return {'postura_f': postura_f, 'postura_c':postura_c,
                'porc_f':porcentaje_f, 'porc_c':porcentaje_c}

@receiver(post_save, sender=Postura)
def crea_notificacion(sender, instance, **kwargs):
    if kwargs['created']:
        debate = instance['id_debate']
        id_creador = debate.id_usuario_id
        num_postura = Postura.objects.filter(id_debate=debate.id_debate).count()
        try:
            notificacion = Notificacion.objects.get(id_debate_id=debate.id_debate, tipo="postura")
            print("segunda o mas")
            notificacion.mensaje = str(num_postura)+" usuarios han definido postura en "+str(debate)
            notificacion.estado = 0
            notificacion.save()
        except:
            print("primera")
            msj = str(num_postura)+" usuario ha definido postura en "+str(debate)
            notificacion = Notificacion.objects.create(id_debate = debate, mensaje=msj)
        Group("notificacion").send({"text": str(id_creador)})

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
    def as_dict(self):
        if self.alias_c == "username":
            usr = User.objects.get(id = self.id_usuario.id).username
        else:
            usr = Perfil.objects.get(user_id = self.id_usuario.id).alias

        return {'descripcion': self.descripcion, 'nombre': usr, 'postura': self.postura}

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
    tipo_valoracion = models.CharField(max_length=50, default='nulo')
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
    id_usuario = models.ForeignKey(User)
    id_argumento = models.ForeignKey(Argumento)


    def __unicode__(self): # __unicode__ on Python 2
        return self.descripcion_edicion
