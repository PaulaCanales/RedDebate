# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-08-05 04:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0008_notificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='tipo',
            field=models.CharField(default='postura', max_length=50),
        ),
    ]