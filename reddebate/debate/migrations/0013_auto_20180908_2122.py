# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-08 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0012_visita_id_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visita',
            name='num',
            field=models.IntegerField(default=1),
        ),
    ]
