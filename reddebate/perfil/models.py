from __future__ import unicode_literals
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from datetime import *
from django.db import models

from resumen.models import Debate

def unique_rand():
    while True:
        code = User.objects.make_random_password(length=4)
        alias = "anonimo_"+code
        if not Perfil.objects.filter(alias=alias).exists():
            return alias

# Create your models here.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    alias = models.CharField(max_length=30, null=False, unique=True, default=unique_rand, error_messages={'unique':"Ya existe un perfil con este Alias"})
    reputacion = models.IntegerField(default=0, blank=True)
