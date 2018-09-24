# coding=utf-8
from __future__ import unicode_literals
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from datetime import *
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from resumen.models import Debate
from perfil.models import Profile, Notification
from channels import Group
import json

# Create your models here.

class Position(models.Model):
    #parametros de la tabla.
    id_position = models.AutoField(primary_key=True)
    position = models.IntegerField(default=1)
    change = models.IntegerField(default=0)
    count_change = models.IntegerField(default=0)
    date = models.DateField(default=datetime.now)
    id_user = models.ForeignKey(User)
    id_debate = models.ForeignKey(Debate)

    def __unicode__(self): # __unicode__ on Python 2
        return unicode(self.position)
    def __getitem__(self, key):
        return getattr(self, key)
    def as_dict(self):
        infavor_position=Position.objects.filter(id_debate_id=self.id_debate, position=1).count()
        against_position=Position.objects.filter(id_debate_id=self.id_debate, position=0).count()
        if (int(infavor_position+against_position)==0):
            infavor_percent=0
            against_percent=0
        else:
            infavor_percent=round(float(infavor_position) / float(against_position+infavor_position),3)*100
            against_percent=round(float(against_position) / float(against_position+infavor_position),3)*100
        return {'infavor_position': infavor_position, 'against_position':against_position,
                'infavor_percent':infavor_percent, 'against_percent':against_percent}

@receiver(post_save, sender=Position)
def notificatePosition(sender, instance, **kwargs):
    if kwargs['created']:
        debate = instance['id_debate']
        id_owner = debate.id_user_id
        positions_num = Position.objects.filter(id_debate=debate.id_debate).count()
        title = '"'+unicode(debate.title)+'"'
        try:
            notification = Notification.objects.get(id_debate_id=debate.id_debate, id_user_id=id_owner, type="position")
            print("segunda o mas")
            notification.message = str(positions_num)+" usuarios han definido postura en "+title
            notification.state = 0
            notification.date = datetime.now()
            notification.save()
        except:
            print("primera")
            msj = str(positions_num)+" user ha definido postura en "+title
            notification = Notification.objects.create(id_debate = debate, id_user_id=id_owner, message=msj, type="position")
        Group("notification").send({'text': json.dumps(
                                            {'id_owner': str(id_owner),
                                            'message': notification.message,
                                            'id_notification': notification.id,
                                            'id_debate': debate.id_debate
                                            })})

class Argumento(models.Model):
    #parametros de la tabla.
    id_argument = models.AutoField(primary_key=True)
    text = models.CharField(max_length=300)
    position = models.IntegerField(default=1)
    owner_type = models.CharField(max_length=50, default='username')
    date = models.DateField(default=datetime.now)
    id_user = models.ForeignKey(User)
    id_debate = models.ForeignKey(Debate)
    score = models.IntegerField(default=0)

    def __unicode__(self): # __unicode__ on Python 2
        return self.text
    def __getitem__(self, key):
        return getattr(self, key)
    def as_dict(self):
        if self.owner_type == "username":
            usr = User.objects.get(id = self.id_user.id).username
        else:
            usr = Profile.objects.get(user_id = self.id_user.id).alias

        return {'text': self.text, 'name': usr, 'position': self.position}

@receiver(post_save, sender=Argumento)
def notificateArgument(sender, instance, **kwargs):
    if kwargs['created']:
        argument = instance['id_argument']
        debate = instance['id_debate']
        id_owner = debate.id_user_id
        title = '"'+unicode(debate.title)+'"'
        argument_num = Argumento.objects.filter(id_debate=debate.id_debate).count()
        try:
            notification = Notification.objects.get(id_debate_id=debate.id_debate, id_user_id=id_owner, type="argument")
            print("segunda o mas")
            notification.message = str(argument_num)+" usuarios han argumentado en "+title
            notification.state = 0
            notification.date = datetime.now()
            notification.save()
        except:
            print("primera")
            msj = str(argument_num)+" user ha argumentado en "+title
            notification = Notification.objects.create(id_debate = debate, id_user_id=id_owner, message=msj, type="argument")
        Group("notification").send({'text': json.dumps(
                                            {'id_owner': str(id_owner),
                                            'message': notification.message,
                                            'id_notification': notification.id,
                                            'id_debate': debate.id_debate
                                            })})

class Counterargument(models.Model):
    #parametros de la tabla.
    id_counterarg = models.AutoField(primary_key=True)
    text = models.CharField(max_length=300)
    owner_type = models.CharField(max_length=50, default='username')
    date = models.DateField(default=datetime.now)
    id_user = models.ForeignKey(User)
    id_argument = models.ForeignKey(Argumento)

    def __getitem__(self, key):
        return getattr(self, key)
    def __unicode__(self): # __unicode__ on Python 2
        return self.text

@receiver(post_save, sender=Counterargument)
def notificateCounterarg(sender, instance, **kwargs):
    argument = instance['id_argument']
    debate = argument.id_debate
    id_owner = argument.id_user_id
    arg_text = unicode(argument.text)
    text = '"'+(arg_text[:30] + '..') if len(arg_text) > 75 else arg_text +'"'
    try:
        notification = Notification.objects.get(id_debate_id=debate.id_debate, id_user_id=id_owner, type="rebate")
        print("segunda o mas")
        notification.message = "Han rebatido tu agumento: "+(text)
        notification.state = 0
        notification.date = datetime.now()
        notification.save()
    except:
        print("primera")
        msj = "Han rebatido tu argumento: "+(text)
        notification = Notification.objects.create(id_debate = debate, id_user_id=id_owner, message=msj, type="rebate")
    Group("notification").send({'text': json.dumps(
                                        {'id_owner': str(id_owner),
                                        'message': notification.message,
                                        'id_notification': notification.id,
                                        'id_debate': debate.id_debate
                                        })})

class Rate(models.Model):
    #parametros de la tabla.
    id_rate = models.AutoField(primary_key=True)
    rate_type = models.CharField(max_length=50, default='none')
    date = models.DateField(default=datetime.now)
    id_user = models.ForeignKey(User)
    id_argument = models.ForeignKey(Argumento)

    def __getitem__(self, key):
        return getattr(self, key)
    def __unicode__(self): # __unicode__ on Python 2
        return self.id_rate

@receiver(post_save, sender=Rate)
def notificateRate(sender, instance, **kwargs):
    argument = instance['id_argument']
    debate = argument.id_debate
    id_owner = argument.id_user_id
    arg_text = unicode(argument.text)
    text = '"'+(arg_text[:30] + '..') if len(arg_text) > 75 else arg_text+'"'
    try:
        notification = Notification.objects.get(id_debate_id=debate.id_debate, id_user_id=id_owner, type="valoracion")
        print("segunda o mas")
        notification.message = "Han valorado tu argument: "+(text)
        notification.state = 0
        notification.date = datetime.now()
        notification.save()
    except:
        print("primera")
        msj = "Han valorado tu argument: "+(text)
        notification = Notification.objects.create(id_debate = debate, id_user_id=id_owner, message=msj, type="valoracion")
    Group("notification").send({'text': json.dumps(
                                        {'id_owner': str(id_owner),
                                        'message': notification.message,
                                        'id_notification': notification.id,
                                        'id_debate': debate.id_debate
                                        })})

class PrivateMembers(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User)
    id_debate = models.ForeignKey(Debate)
    def __unicode__(self): # __unicode__ on Python 2
		return self.id
    def __getitem__(self, key):
        return getattr(self, key)
    def as_dict(self, list):
        return {'members': list, 'id': self.id}

@receiver(post_save, sender=PrivateMembers)
def notificatePrivateMembers(sender, instance, **kwargs):
    debate = instance['id_debate']
    id_owner = instance['id_user'].id
    title = '"'+unicode(debate.title)+'"'
    if debate.id_user_id != id_owner:
        try:
            notification = Notification.objects.get(id_debate_id=debate.id_debate, id_user_id=id_owner, type="debprivado")
            print("segunda o mas")
            notification.message = "Te han agregado un debate privado: "+title
            notification.state = 0
            notification.date = datetime.now()
            notification.save()
        except:
            print("primera")
            msj = "Te han agregado un debate privado: "+title
            notification = Notification.objects.create(id_debate = debate, id_user_id=id_owner, message=msj, type="debprivado")
        Group("notification").send({'text': json.dumps(
                                            {'id_owner': str(id_owner),
                                            'message': notification.message,
                                            'id_notification': notification.id,
                                            'id_debate': debate.id_debate
                                            })})

class Visit(models.Model):
    #parametros de la tabla.
    id = models.AutoField(primary_key=True)
    num = models.IntegerField(default=1)
    date = models.DateTimeField(default=datetime.now)
    id_debate = models.ForeignKey(Debate)
    id_user = models.ForeignKey(User)

    def __unicode__(self): # __unicode__ on Python 2
        return self.num
