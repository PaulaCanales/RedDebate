# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-16 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0013_auto_20180916_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listado',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]
