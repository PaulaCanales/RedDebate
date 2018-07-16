from __future__ import unicode_literals
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from datetime import *
from django.db import models

from resumen.models import Debate

# Create your models here.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    alias = models.CharField(max_length=30, default="anonimo")
    reputacion = models.IntegerField(default=0, blank=True)
