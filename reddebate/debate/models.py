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

class Argument(models.Model):
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

@receiver(post_save, sender=Argument)
def notificateArgument(sender, instance, **kwargs):
    if kwargs['created']:
        argument = instance['id_argument']
        debate = instance['id_debate']
        id_owner = debate.id_user_id
        title = '"'+unicode(debate.title)+'"'
        argument_num = Argument.objects.filter(id_debate=debate.id_debate).count()
        try:
            notification = Notification.objects.get(id_debate_id=debate.id_debate, id_user_id=id_owner, type="argument")
            notification.message = str(argument_num)+" usuarios han argumentado en "+title
            notification.state = 0
            notification.date = datetime.now()
            notification.save()
        except:
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
    id_argument = models.ForeignKey(Argument)

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
    id_argument = models.ForeignKey(Argument)

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
        notification.message = "Han valorado tu argument: "+(text)
        notification.state = 0
        notification.date = datetime.now()
        notification.save()
    except:
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
    type = models.CharField(max_length=50, default='username')
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
            notification.message = "Te han agregado un debate privado: "+title
            notification.state = 0
            notification.date = datetime.now()
            notification.save()
        except:
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

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    reason = models.IntegerField(default=0)
    type = models.CharField(max_length=50, default='none')
    owner = models.ForeignKey(User)
    debate = models.ForeignKey(Debate, blank = True,null=True)
    argument = models.ForeignKey(Argument, blank = True,null=True)
    counterarg = models.ForeignKey(Counterargument, blank = True,null=True)

    def __unicode__(self): # __unicode__ on Python 2
        return self.id
    def __getitem__(self, key):
        return getattr(self, key)

# @receiver(post_save, sender=Report)
# def notificateReport(sender, instance, **kwargs):
#     type = instance['type']
#     debate = instance['debate']
#     reported = instance['reported']
#     moderator = User.objects.filter(is_staff=1)
#     moderator = User.objects.filter(is_staff=1).values('id')[0]
#     print(moderator['id'])
#     # send_notification = newNotificationReport(type)
#     # NOTIFICAR AL DENUNCIADO
#     # NOTIFICAR AL MODERADOR
#     if type == "argument":
#         arg = instance['argument']
#         arg_num = Report.objects.filter(argument=arg.id_argument).count()
#         arg_text = unicode(arg.text)
#         text = '"'+(arg_text[:30] + '..') if len(arg_text) > 75 else arg_text +'"'
#         reported_msj = "Tienes un argumento en revision: "+tex
#         try:
#             moderador_ntf = Notification.objects.get(id_debate_id=debate.id_debate, id_user_id=moderator['id'], type="report")
#             moderador_ntf.message = "Han reportado"+str(arg_num)+"el argumento: "+text
#             moderador_ntf.state = 0
#             moderador_ntf.date = datetime.now()
#             moderador_ntf.save()
#         except:
#             moderator_msj = "Se ha reportado un argumento malicioso: "+text
#             moderador_ntf = Notification.objects.create(id_debate = debate, id_user_id=moderator['id'], message=moderator_msj, type="report")
#         Group("notification").send({'text': json.dumps(
#                                                 {'id_owner': str(moderator['id']),
#                                                 'message': notification.message,
#                                                 'id_notification': notification.id,
#                                                 'id_debate': debate.id_debate
#                                                 })})
    # elif type == "counterarg":
    #     counterarg = instance['counterarg']
    #
    # id_owner = instance['id_user'].id
    # title = '"'+unicode(debate.title)+'"'
    # if debate.id_user_id != id_owner:
    #     try:
    #         notification = Notification.objects.get(id_debate_id=debate.id_debate, id_user_id=id_owner, type="debprivado")
    #         notification.message = "Te han agregado un debate privado: "+title
    #         notification.state = 0
    #         notification.date = datetime.now()
    #         notification.save()
    #     except:
    #         msj = "Te han agregado un debate privado: "+title
    #         notification = Notification.objects.create(id_debate = debate, id_user_id=id_owner, message=msj, type="debprivado")
    #     Group("notification").send({'text': json.dumps(
    #                                         {'id_owner': str(id_owner),
    #                                         'message': notification.message,
    #                                         'id_notification': notification.id,
    #                                         'id_debate': debate.id_debate
    #                                         })})
