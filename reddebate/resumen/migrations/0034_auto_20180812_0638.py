# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-08-12 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumen', '0033_debate_num_rebate'),
    ]

    operations = [
        migrations.AddField(
            model_name='debate',
            name='num_argumento',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='debate',
            name='num_cambio_postura',
            field=models.IntegerField(default=1),
        ),
    ]