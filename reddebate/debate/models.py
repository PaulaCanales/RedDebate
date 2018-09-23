# coding=utf-8
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
import json

# Create your models here.

class Postura(models.Model):
    #parametros de la tabla.
    id_postura = models.AutoField(primary_key=True)
    postura = models.IntegerField(default=1)
    cambio_postura = models.IntegerField(default=0)
    cuenta_cambios = models.IntegerField(default=0)
    date_Postura = models.DateField(default=datetime.now)
    id_usuario = models.ForeignKey(User)
    id_debate = models.ForeignKey(Debate)

    def __unicode__(self): # __unicode__ on Python 2
        return unicode(self.postura)
    def __getitem__(self, key):
        return getattr(self, key)
    def as_dict(self):
        # id_creador = Debate.objects.get(id_debate=self.id_debate.id_debate).id_usuario_id
        postura_f=Postura.objects.filter(id_debate_id=self.id_debate, postura=1).count()
        postura_c=Postura.objects.filter(id_debate_id=self.id_debate, postura=0).count()
        if (int(postura_f+postura_c)==0):
            infavor_percent=0
            against_percent=0
        else:
            infavor_percent=round(float(postura_f) / float(postura_c+postura_f),3)*100
            against_percent=round(float(postura_c) / float(postura_c+postura_f),3)*100
        return {'postura_f': postura_f, 'postura_c':postura_c,
                'infavor_percent':infavor_percent, 'against_percent':against_percent}

@receiver(post_save, sender=Postura)
def notificacion_postura(sender, instance, **kwargs):
    if kwargs['created']:
        debate = instance['id_debate']
        id_creador = debate.id_usuario_id
        num_postura = Postura.objects.filter(id_debate=debate.id_debate).count()
        titulo = '"'+unicode(debate.titulo)+'"'
        try:
            notificacion = Notificacion.objects.get(id_debate_id=debate.id_debate, id_usuario_id=id_creador, tipo="postura")
            print("segunda o mas")
            notificacion.mensaje = str(num_postura)+" usuarios han definido postura en "+titulo
            notificacion.estado = 0
            notificacion.fecha = datetime.now()
            notificacion.save()
        except:
            print("primera")
            msj = str(num_postura)+" usuario ha definido postura en "+titulo
            notificacion = Notificacion.objects.create(id_debate = debate, id_usuario_id=id_creador, mensaje=msj, tipo="postura")
        Group("notificacion").send({'text': json.dumps(
                                            {'id_creador': str(id_creador),
                                            'mensaje': notificacion.mensaje,
                                            'id_notificacion': notificacion.id,
                                            'id_debate': debate.id_debate
                                            })})

class Argumento(models.Model):
    #parametros de la tabla.
    id_argumento = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=300)
    postura = models.IntegerField(default=1)
    alias_c = models.CharField(max_length=50, default='username')
    date_argumento = models.DateField(default=datetime.now)
    id_usuario = models.ForeignKey(User)
    id_debate = models.ForeignKey(Debate)
    puntaje = models.IntegerField(default=0)

    def __unicode__(self): # __unicode__ on Python 2
        return self.descripcion
    def __getitem__(self, key):
        return getattr(self, key)
    def as_dict(self):
        if self.alias_c == "username":
            usr = User.objects.get(id = self.id_usuario.id).username
        else:
            usr = Perfil.objects.get(user_id = self.id_usuario.id).alias

        return {'descripcion': self.descripcion, 'nombre': usr, 'postura': self.postura}

@receiver(post_save, sender=Argumento)
def notificacion_argumento(sender, instance, **kwargs):
    if kwargs['created']:
        argumento = instance['id_argumento']
        debate = instance['id_debate']
        id_creador = debate.id_usuario_id
        titulo = '"'+unicode(debate.titulo)+'"'
        argument_num = Argumento.objects.filter(id_debate=debate.id_debate).count()
        try:
            notificacion = Notificacion.objects.get(id_debate_id=debate.id_debate, id_usuario_id=id_creador, tipo="argumento")
            print("segunda o mas")
            notificacion.mensaje = str(argument_num)+" usuarios han argumentado en "+titulo
            notificacion.estado = 0
            notificacion.fecha = datetime.now()
            notificacion.save()
        except:
            print("primera")
            msj = str(argument_num)+" usuario ha argumentado en "+titulo
            notificacion = Notificacion.objects.create(id_debate = debate, id_usuario_id=id_creador, mensaje=msj, tipo="argumento")
        Group("notificacion").send({'text': json.dumps(
                                            {'id_creador': str(id_creador),
                                            'mensaje': notificacion.mensaje,
                                            'id_notificacion': notificacion.id,
                                            'id_debate': debate.id_debate
                                            })})

class Respuesta(models.Model):
    #parametros de la tabla.
    id_respuesta = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=300)
    alias_c = models.CharField(max_length=50, default='username')
    date_respuesta = models.DateField(default=datetime.now)
    id_usuario = models.ForeignKey(User)
    id_argumento = models.ForeignKey(Argumento)

    def __getitem__(self, key):
        return getattr(self, key)
    def __unicode__(self): # __unicode__ on Python 2
        return self.descripcion

@receiver(post_save, sender=Respuesta)
def notificacion_rebate(sender, instance, **kwargs):
    argumento = instance['id_argumento']
    debate = argumento.id_debate
    id_creador = argumento.id_usuario_id
    texto = unicode(argumento.descripcion)
    descripcion = '"'+(texto[:30] + '..') if len(texto) > 75 else texto +'"'
    try:
        notificacion = Notificacion.objects.get(id_debate_id=debate.id_debate, id_usuario_id=id_creador, tipo="rebate")
        print("segunda o mas")
        notificacion.mensaje = "Han rebatido tu argumento: "+(descripcion)
        notificacion.estado = 0
        notificacion.fecha = datetime.now()
        notificacion.save()
    except:
        print("primera")
        msj = "Han rebatido tu argumento: "+(descripcion)
        notificacion = Notificacion.objects.create(id_debate = debate, id_usuario_id=id_creador, mensaje=msj, tipo="rebate")
    Group("notificacion").send({'text': json.dumps(
                                        {'id_creador': str(id_creador),
                                        'mensaje': notificacion.mensaje,
                                        'id_notificacion': notificacion.id,
                                        'id_debate': debate.id_debate
                                        })})

class Valoracion(models.Model):
    #parametros de la tabla.
    id_valoracion = models.AutoField(primary_key=True)
    tipo_valoracion = models.CharField(max_length=50, default='nulo')
    date_valoracion = models.DateField(default=datetime.now)
    id_usuario = models.ForeignKey(User)
    id_argumento = models.ForeignKey(Argumento)

    def __getitem__(self, key):
        return getattr(self, key)
    def __unicode__(self): # __unicode__ on Python 2
        return self.id_valoracion

@receiver(post_save, sender=Valoracion)
def notificacion_valoracion(sender, instance, **kwargs):
    argumento = instance['id_argumento']
    debate = argumento.id_debate
    id_creador = argumento.id_usuario_id
    texto = unicode(argumento.descripcion)
    descripcion = '"'+(texto[:30] + '..') if len(texto) > 75 else texto+'"'
    try:
        notificacion = Notificacion.objects.get(id_debate_id=debate.id_debate, id_usuario_id=id_creador, tipo="valoracion")
        print("segunda o mas")
        notificacion.mensaje = "Han valorado tu argumento: "+(descripcion)
        notificacion.estado = 0
        notificacion.fecha = datetime.now()
        notificacion.save()
    except:
        print("primera")
        msj = "Han valorado tu argumento: "+(descripcion)
        notificacion = Notificacion.objects.create(id_debate = debate, id_usuario_id=id_creador, mensaje=msj, tipo="valoracion")
    Group("notificacion").send({'text': json.dumps(
                                        {'id_creador': str(id_creador),
                                        'mensaje': notificacion.mensaje,
                                        'id_notificacion': notificacion.id,
                                        'id_debate': debate.id_debate
                                        })})

class Edicion(models.Model):
    #parametros de la tabla.
    id_edicion = models.AutoField(primary_key=True)
    descripcion_edicion = models.CharField(max_length=300)
    date_edicion = models.DateTimeField(default=datetime.now)
    id_usuario = models.ForeignKey(User)
    id_argumento = models.ForeignKey(Argumento)


    def __unicode__(self): # __unicode__ on Python 2
        return self.descripcion_edicion

class Participantes(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(User)
    id_debate = models.ForeignKey(Debate)
    def __unicode__(self): # __unicode__ on Python 2
		return self.id
    def __getitem__(self, key):
        return getattr(self, key)
    def as_dict(self, lista):
        return {'usuario_participa': lista, 'id': self.id}

@receiver(post_save, sender=Participantes)
def notificacion_participantes(sender, instance, **kwargs):
    debate = instance['id_debate']
    id_creador = instance['id_usuario'].id
    titulo = '"'+unicode(debate.titulo)+'"'
    if debate.id_usuario_id != id_creador:
        try:
            notificacion = Notificacion.objects.get(id_debate_id=debate.id_debate, id_usuario_id=id_creador, tipo="debprivado")
            print("segunda o mas")
            notificacion.mensaje = "Te han agregado un debate privado: "+titulo
            notificacion.estado = 0
            notificacion.fecha = datetime.now()
            notificacion.save()
        except:
            print("primera")
            msj = "Te han agregado un debate privado: "+titulo
            notificacion = Notificacion.objects.create(id_debate = debate, id_usuario_id=id_creador, mensaje=msj, tipo="debprivado")
        Group("notificacion").send({'text': json.dumps(
                                            {'id_creador': str(id_creador),
                                            'mensaje': notificacion.mensaje,
                                            'id_notificacion': notificacion.id,
                                            'id_debate': debate.id_debate
                                            })})

class Visita(models.Model):
    #parametros de la tabla.
    id = models.AutoField(primary_key=True)
    num = models.IntegerField(default=1)
    date = models.DateTimeField(default=datetime.now)
    id_debate = models.ForeignKey(Debate)
    id_usuario = models.ForeignKey(User)

    def __unicode__(self): # __unicode__ on Python 2
        return self.num
