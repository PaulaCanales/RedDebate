# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-11 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumen', '0017_auto_20170103_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debate',
            name='titulo',
            field=models.CharField(max_length=100),
        ),
    ]
