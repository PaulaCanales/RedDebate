# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-16 01:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0008_postura_cuenta_cambios'),
    ]

    operations = [
        migrations.AddField(
            model_name='argumento',
            name='puntaje',
            field=models.IntegerField(default=0),
        ),
    ]