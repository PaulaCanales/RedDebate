# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-07-15 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumen', '0023_remove_argumento_usa_alias'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='reputacion',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]