# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-16 03:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0012_auto_20180914_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listado',
            name='nombre',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
