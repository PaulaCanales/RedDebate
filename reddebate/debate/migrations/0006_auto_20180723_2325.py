# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-07-23 23:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0005_postura_cambio_postura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postura',
            name='cambio_postura',
            field=models.IntegerField(default=0),
        ),
    ]