# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 21:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumen', '0005_auto_20161124_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postura',
            name='postura',
            field=models.IntegerField(default=1),
        ),
    ]